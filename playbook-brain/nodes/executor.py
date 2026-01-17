from typing import Dict, Any, List
from langchain_core.messages import AIMessage
from pydantic import BaseModel, Field
from graph.state import AgentState
from .llm_utils import get_llm

# --- Data Models ---

class PositionUpdate(BaseModel):
    """Structure for manual player adjustments"""
    player_id: str = Field(..., description="The ID of the player to move (e.g., 'lal-lebron-james')")
    x: float = Field(..., description="The new X coordinate (0-800)")
    y: float = Field(..., description="The new Y coordinate (0-500)")

class AdjustmentOutput(BaseModel):
    moves: List[PositionUpdate]

# --- Helper: Role Mapper ---

def _map_roles_to_ids(players: List[Dict]) -> Dict[str, str]:
    """
    Creates a map like: {'PG': 'okc-shai...', 'C': 'okc-chet...'}
    This allows the playbook to use abstract roles while we move real IDs.
    """
    role_map = {}
    # Filter only offensive players for the offensive playbook
    offense_players = [p for p in players if p['data'].get('side') == 'ATTACK']
    
    # Simple mapping based on the 'position' field we stored in Setup
    for p in offense_players:
        pos = p['data'].get('position') # e.g., 'PG', 'C'
        if pos:
            role_map[pos] = p['id']
            
    return role_map

# --- The Node Logic ---

def executor_node(state: AgentState) -> Dict[str, Any]:
    """
    The 'Hands' of the system.
    Responsible for actually mutating the 'players' state.
    Handles:
    1. Running a Set Play (Playbook) -> Maps Roles to IDs.
    2. Manual Adjustment (ADJUST) -> Uses LLM to parse intent.
    3. BALL PHYSICS -> Ensures ball moves with the handler.
    """
    intent = state.get("intent")
    current_players = state.get("players", [])
    
    # State variables for the ball
    current_ball_handler = state.get("ball_handler_id")
    current_ball_pos = state.get("ball_position")
    
    updates_map = {} # Stores target positions: {player_id: {x, y}}
    new_ball_handler = current_ball_handler # Default to keeping same handler
    
    action_description = ""

    # ---------------------------------------------------------
    # Case A: Execute a Pre-defined Play (Template -> Real IDs)
    # ---------------------------------------------------------
    if intent == "PLAYBOOK":
        play = state.get("selected_play")
        current_step_index = state.get("current_step_index", 0)  # ✅ התחל מ-0
        
        if play and "steps" in play:
            total_steps = len(play["steps"])
            
            if current_step_index < total_steps:
                step_data = play["steps"][current_step_index]
                
                # 1. Update Player Positions
                for player_pos in step_data:
                    player_id = player_pos.get("id")
                    if player_id and player_id != "ball":
                        updates_map[player_id] = {"x": player_pos["x"], "y": player_pos["y"]}
                    elif player_id == "ball":
                        current_ball_pos = {"x": player_pos["x"], "y": player_pos["y"]}
                        ball_pos_in_step = current_ball_pos

                # 2. Determine Ball Handler
                if ball_pos_in_step:
                    for player_pos in step_data:
                        player_id = player_pos.get("id")
                        if player_id and player_id != "ball":
                            if (player_pos["x"] == ball_pos_in_step["x"] and 
                                player_pos["y"] == ball_pos_in_step["y"]):
                                new_ball_handler = player_id
                                break

                # ✅ בנה את הרשימה המעודכנת כאן (לפני ה-return!)
                updated_players_list = []
                final_ball_pos = current_ball_pos
                
                for player in current_players:
                    p_id = player["id"]
                    new_props = player.copy()
                    
                    if p_id in updates_map:
                        new_props["position"] = updates_map[p_id]
                    
                    if p_id == new_ball_handler:
                        final_ball_pos = new_props["position"]
                        
                    updated_players_list.append(new_props)

                # עכשיו אפשר לעשות return עם המשתנים הנכונים
                next_step_index = current_step_index + 1
                
                if next_step_index < total_steps:
                    action_description = f"Running {play['name']}: Step {current_step_index + 1}/{total_steps}. Continuing..."
                    return {
                        "players": updated_players_list,  # ✅ עכשיו זה קיים!
                        "ball_position": final_ball_pos,  # ✅ עכשיו זה קיים!
                        "ball_handler_id": new_ball_handler,
                        "current_step_index": next_step_index,
                        "intent": "PLAYBOOK",
                        "messages": [AIMessage(content=action_description)]
                    }
                else:
                    action_description = f"Running {play['name']}: Step {current_step_index + 1}/{total_steps}. Complete!"
                    return {
                        "players": updated_players_list,  # ✅ עכשיו זה קיים!
                        "ball_position": final_ball_pos,  # ✅ עכשיו זה קיים!
                        "ball_handler_id": new_ball_handler,
                        "current_step_index": 0,
                        "messages": [AIMessage(content=action_description)]
                    }
                            
    # ---------------------------------------------------------
    # Case B: Manual Adjustment (Natural Language -> IDs)
    # ---------------------------------------------------------
    elif intent == "ADJUST":
        llm = get_llm()
        user_command = state["messages"][-1].content
        
        # Context for the LLM
        player_list_str = "\n".join([f"- {p['id']} ({p['data']['name']}, {p['data']['position']})" for p in current_players])
        
        adjust_prompt = f"""
        You are the Physics Engine. Move the requested players.
        
        **Current Roster IDs:**
        {player_list_str}
        
        **Court Key:** Top(400,400), Paint(400,100), LeftCorner(50,50), RightCorner(750,50).
        
        **Command:** "{user_command}"
        
        Return the exact IDs and new X,Y coordinates.
        """
        
        structured_llm = llm.with_structured_output(AdjustmentOutput)
        result = structured_llm.invoke(adjust_prompt)
        
        for move in result.moves:
            updates_map[move.player_id] = {"x": move.x, "y": move.y}
            
        action_description = "Manual adjustment executed."

    # ---------------------------------------------------------
    # Apply Updates & Sync Ball
    # ---------------------------------------------------------
    
    updated_players_list = []
    final_ball_pos = current_ball_pos
    
    for player in current_players:
        p_id = player["id"]
        new_props = player.copy()
        
        # 1. Update Position if needed
        if p_id in updates_map:
            new_props["position"] = updates_map[p_id]
        
        # 2. Check Ball Physics
        # If this player is the Ball Handler (new or old), the ball goes to them
        if p_id == new_ball_handler:
            # We attach the ball to the player's new position
            final_ball_pos = new_props["position"]
            
        updated_players_list.append(new_props)

    return {
        "players": updated_players_list,
        "ball_position": final_ball_pos,
        "ball_handler_id": new_ball_handler,
        "messages": [AIMessage(content=f"{action_description}")]
    }