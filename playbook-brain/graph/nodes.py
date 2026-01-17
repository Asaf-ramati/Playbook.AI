from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage
from .state import AgentState
import os
from typing import Dict, Any, Literal, Optional
from pydantic import BaseModel, Field
from .roster import get_team_roster, get_player_by_id,  MOCK_DB
from .geometry import identify_zone, analyze_spacing
from coach.playbook import PLAYBOOK

def get_llm():
    """Lazy load the LLM to ensure env vars are loaded first"""
    return ChatOpenAI(model="gpt-4o", api_key=os.getenv("OPENAI_API_KEY"))

def analyzer_node(state: AgentState) -> Dict[str, Any]:
    """
    Analyzes the court state using two layers:
    1. Deterministic Layer: Geometry calculations & Roster data lookup.
    2. Strategic Layer: LLM analysis based on the enriched data.
    """
    # Extract raw player data from the shared state
    raw_players = state.get('players', [])
    
    # --- Step 1: Load Team Rosters ---
    # In a real scenario, we would determine which teams are playing from the state.
    # For now, we load our mock data.
    lakers_roster = get_team_roster("lakers_mock")
    warriors_roster = get_team_roster("warriors_mock")
    full_roster = lakers_roster + warriors_roster
    
    # --- Step 2: Geometric Analysis (Spacing) ---
    # Calculate spacing score and identify clogged areas
    spacing_data = analyze_spacing(raw_players)
    
    # --- Step 3: Data Enrichment (Contextual Snapshot) ---
    # Create a text representation that combines location (Geometry) with skill (Roster)
    tactical_snapshot = []
    
    for p in raw_players:
        # Identify the geometric zone (e.g., 'CORNER_3', 'PAINT')
        zone = identify_zone(p['position'])
        
        # Fetch player profile to understand capabilities
        profile = get_player_by_id(p['id'], full_roster)
        
        if profile:
            # Logic: Check if the player is in their effective shooting range
            # We treat 'TOP_3' as a valid 3pt spot
            is_in_range = zone in profile['shooting_ranges'] or \
                          (zone == "TOP_3" and "3pt" in profile['shooting_ranges'])
            
            position_status = "Effective Range" if is_in_range else "OUT OF POSITION"
            
            # Format the info string for the LLM
            info = (
                f"- {profile['name']} ({profile['position']}) | "
                f"Loc: {zone} | Role: {profile['archetype']} | "
                f"Status: {position_status}"
            )
        else:
            # Fallback for unknown players
            info = f"- Unknown Player ({p['id']}) at {zone}"
            
        tactical_snapshot.append(info)

    snapshot_text = "\n".join(tactical_snapshot)

    # --- Step 4: LLM Tactical Analysis ---
    # We prompt the model to act as an elite scout, focusing on actionable insights.
    analysis_prompt = f"""
    You are an elite NBA Tactical Scout. Analyze the current snapshot derived from optical tracking data.

    **Global Metrics:**
    - Spacing Score: {spacing_data['score']}/10
    - Clogged Areas: {', '.join(spacing_data['clogged_pairs']) if spacing_data['clogged_pairs'] else "None"}

    **Player Detail (Position & Context):**
    {snapshot_text}

    **Your Task:**
    Provide a concise analysis focusing on:
    1. **Offensive Flows:** Who is well-positioned? Who is clogging the paint?
    2. **Mismatches/Opportunities:** Is a non-shooter outside? Is a slasher open in the paint?
    3. **Immediate Recommendation:** One sentence on what should happen next.

    Keep it professional, concise, and tactical.
    """

    llm = get_llm()
    response = llm.invoke([{"role": "user", "content": analysis_prompt}])
    
    # Debug log to see what the agent "sees"
    print(f"--- ANALYZER OUTPUT ---\n{response.content}\n-----------------------")

    # Update the state with the enriched analysis
    return {
        "analysis": {
            "spacing_score": spacing_data['score'],
            "is_clogged": spacing_data['is_clogged'],
            "tactical_summary": response.content,
            "snapshot_text": snapshot_text, # Saved for the Consultant node
            "player_count": len(raw_players)
        }
    }

class RouterDecision(BaseModel):
    """
    Represents the strict decision structure the Router must return.
    This ensures the graph always knows exactly where to go next.
    """
    intent: Literal["CONSULT", "PLAYBOOK", "ADJUST"] = Field(
        ..., 
        description="The determined intent: 'CONSULT' for advice/questions, 'PLAYBOOK' to run a set play, 'ADJUST' for manual commands."
    )
    play_id: Optional[str] = Field(
        None, 
        description="If intent is PLAYBOOK, this MUST be one of the keys provided in the context. If no specific play matches, select the most tactical fit."
    )
    reasoning: str = Field(
        ..., 
        description="A brief explanation of why this intent and play (if any) were chosen."
    )

def router_node(state: AgentState) -> Dict[str, Any]:
    """
    The Decision Unit.
    It takes the User's input and the Analyzer's insights to decide on the next step.
    It does NOT modify the players; it only routes the flow.
    """
    llm = get_llm()
    
    # Bind the Pydantic model to the LLM to force JSON output
    structured_llm = llm.with_structured_output(RouterDecision)
    
    # Prepare context for the prompt
    user_message = state['messages'][-1].content
    tactical_summary = state.get('analysis', {}).get('tactical_summary', 'No analysis available')
    
    # Inject available plays so the LLM knows what's possible
    # We replace underscores with spaces for better readability in the prompt
    available_plays_str = ", ".join(PLAYBOOK.keys())
    
    router_prompt = f"""
    You are the Head Coach Logic Unit. Your goal is to determine the user's intent.

    **Context:**
    1. User Message: "{user_message}"
    2. Court Tactical Analysis: {tactical_summary}
    3. Available Plays in Database: [{available_plays_str}]

    **Decision Logic:**
    
    A. **CONSULT**: Return this if the user asks a question, wants an opinion, asks "what if", or discusses strategy without asking to move players.
       - Example: "What do you think about the spacing?"
       - Example: "Who should take the last shot?"

    B. **PLAYBOOK**: Return this if the user wants to execute a play, run a set, or if the user asks for a solution that requires moving the team.
       - You MUST try to map the request to one of the 'Available Plays'.
       - If the user says "Run a play" without specifying, pick the best play ID based on the Court Tactical Analysis.
       - Example: "Run a Pick and Roll." -> intent: PLAYBOOK, play_id: "PICK_AND_ROLL_TOP"

    C. **ADJUST**: Return this if the user gives a specific, manual command to move specific players.
       - Example: "Move LeBron to the corner."
       - Example: "Push the defense back."

    **Output Requirement:**
    Return a valid JSON object matching the RouterDecision schema.
    """
    
    # Invoke the LLM
    decision = structured_llm.invoke(router_prompt)
    
    # Log the decision for debugging purposes
    print(f"--- ROUTER DECISION: {decision.intent} | Play: {decision.play_id} | Reason: {decision.reasoning} ---")
    
    # Update the state with the decision variables
    return {
        "intent": decision.intent,
        "target_play": decision.play_id
    }
def consultant_node(state: AgentState) -> Dict[str, Any]:
    """
    The 'Mouth' of the AI Coach.
    Generates expert tactical advice based on the Analyzer's insights.
    This node does NOT modify player positions.
    """
    llm = get_llm()
    
    # Retrieve the rich context generated by the Analyzer
    analysis_context = state.get("analysis", {})
    
    # "snapshot_text" contains the fused data (Location + Skill)
    # e.g., "LeBron James (SF) | Loc: PAINT | Role: Point Forward | Status: Effective Range"
    snapshot_text = analysis_context.get("snapshot_text", "No player data available.")
    tactical_summary = analysis_context.get("tactical_summary", "")
    spacing_score = analysis_context.get("spacing_score", "N/A")
    
    # The user's specific question
    user_question = state['messages'][-1].content
    
    consultant_prompt = f"""
    You are an expert NBA Assistant Coach having a conversation with the Head Coach (the user).
    
    **Current Situation on the Board:**
    - Spacing Grade: {spacing_score}/10
    - Tactical Summary: {tactical_summary}
    
    **Detailed Player Positioning:**
    {snapshot_text}
    
    **User's Question/Comment:**
    "{user_question}"
    
    **Instructions:**
    1. Answer the user's question directly and professionally.
    2. Use the "Player Positioning" data to back up your claims. 
       - Example: Instead of saying "The center is out of position", say "Anthony Davis is clogging the spacing at the 3-point line."
    3. Keep it conversational but concise (max 2-3 sentences unless asked for a detailed breakdown).
    4. If the user suggests a bad idea, explain *why* based on the player's skills (e.g., "That might not work because Gobert can't shoot threes").
    
    Provide your expert advice now.
    """
    
    # Generate the response
    response = llm.invoke([{"role": "user", "content": consultant_prompt}])
    
    # Return the message to be displayed in the chat
    return {
        "messages": [AIMessage(content=response.content)]
    }
# --- Playbook Selector Node ---

def playbook_selector_node(state: AgentState) -> Dict[str, Any]:
    """
    The Librarian.
    Retrieves the specific play details from the static PLAYBOOK database.
    It prepares the data for the Executor but does NOT move players yet.
    """
    play_id = state.get("target_play")
    
    # Attempt to retrieve the play
    selected_play = PLAYBOOK.get(play_id)
    
    # Fallback logic if the Router selected a non-existent play
    if not selected_play:
        # Default to basic spacing if the specific play isn't found
        selected_play = PLAYBOOK.get("BASIC_SPACING") 
        msg = f"Could not find exact play '{play_id}', defaulting to Basic Spacing."
    else:
        msg = f"Preparing to execute: {selected_play['name']}..."

    # We return 'selected_play' so the Executor can access it
    return {
        "selected_play": selected_play,
        "messages": [AIMessage(content=msg)]
    }


# --- Executor Node (The Hands) ---

class PositionUpdate(BaseModel):
    """Structure for manual player adjustments"""
    player_id: str = Field(..., description="The ID of the player to move (e.g., 'team1-sf')")
    x: float = Field(..., description="The new X coordinate (0-800)")
    y: float = Field(..., description="The new Y coordinate (0-500)")

def executor_node(state: AgentState) -> Dict[str, Any]:
    """
    The 'Hands' of the system.
    Responsible for actually mutating the 'players' state.
    Handles two cases:
    1. Running a Set Play (from Playbook).
    2. Manual Adjustment (ADJUST intent).
    """
    intent = state.get("intent")
    current_players = state.get("players", [])
    updates_map = {} # Will store {player_id: {x, y}}
    
    # Case A: Execute a Pre-defined Play
    if intent == "PLAYBOOK":
        play = state.get("selected_play")
        if play and "steps" in play:
            # For now, we execute the first step immediately.
            # In a future version, we could manage step iteration.
            next_positions = play["steps"][0]
            updates_map = {p["id"]: {"x": p["x"], "y": p["y"]} for p in next_positions}
            action_description = f"Executing: {play['name']}"
        else:
            return {"messages": [AIMessage(content="Error: No valid play found to execute.")]}

    # Case B: Manual Adjustment (Natural Language to Coordinates)
    elif intent == "ADJUST":
        llm = get_llm()
        user_command = state["messages"][-1].content
        
        # We need a mini-agent to translate "Move LeBron to the corner" into coordinates
        # We provide the current player list so it knows IDs
        player_list_str = ", ".join([f"{p['id']} ({p.get('data',{}).get('name', 'Unknown')})" for p in current_players])
        
        adjust_prompt = f"""
        You are a Motion Physics Engine. Translate the user's command into specific X,Y coordinates.
        
        **Court Dimensions:** X=0-800, Y=0-500. Hoop is at (400, 50).
        **Key Locations:**
        - Top of Key: (400, 300)
        - Left Corner: (50, 50)
        - Right Corner: (750, 50)
        - Paint/Basket: (400, 100)
        
        **Players:** {player_list_str}
        
        **User Command:** "{user_command}"
        
        Return a list of position updates.
        """
        
        # We expect a list of updates (one or more players moving)
        class AdjustmentOutput(BaseModel):
            moves: List[PositionUpdate]
            
        structured_llm = llm.with_structured_output(AdjustmentOutput)
        result = structured_llm.invoke(adjust_prompt)
        
        # Convert result to map
        for move in result.moves:
            updates_map[move.player_id] = {"x": move.x, "y": move.y}
            
        action_description = "Executing manual adjustment..."

    # --- Apply Updates to State ---
    
    updated_players_list = []
    for player in current_players:
        p_id = player["id"]
        # If this player has a new position in our map, update it
        if p_id in updates_map:
            # Create a new player object to ensure immutability/react-flow detection
            new_player = player.copy()
            new_player["position"] = updates_map[p_id]
            updated_players_list.append(new_player)
        else:
            updated_players_list.append(player)

    return {
        "players": updated_players_list,
        "messages": [AIMessage(content=f"{action_description}. Player positions updated.")]
    }