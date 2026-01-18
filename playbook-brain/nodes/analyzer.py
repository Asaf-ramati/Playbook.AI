from typing import Dict, Any
from graph.state import AgentState
from graph.roster import get_team_roster, get_player_by_id
from graph.geometry import identify_zone, analyze_spacing
from .llm_utils import get_llm


def analyzer_node(state: AgentState) -> Dict[str, Any]:
    """
    Analyzes the court state using two layers:
    1. Deterministic Layer: Geometry calculations & Roster data lookup.
    2. Strategic Layer: LLM analysis based on the enriched data.
    """
    # Extract raw player data from the shared state
    raw_players = state.get('players', [])
    
    # --- Step 1: Load Team Rosters ---
    user_team = state.get("user_team")  # "LAL"
    opp_team = state.get("opponent_team")  # "BOS"
    user_roster = get_team_roster(user_team)
    opp_roster = get_team_roster(opp_team)

    full_roster = user_roster + opp_roster
    
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