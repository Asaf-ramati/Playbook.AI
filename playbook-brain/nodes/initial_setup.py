from typing import Dict, Any, List
from langchain_core.messages import AIMessage
from .state import AgentState
from .roster import get_team_roster

# --- Constants (Matching your Frontend) ---

STARTING_POSITIONS_OFFENSE = {
    "PG": {"x": 300, "y": 400}, 
    "SG": {"x": 160, "y": 320},
    "SF": {"x": 440, "y": 320},
    "PF": {"x": 180, "y": 50}, 
    "C":  {"x": 400, "y": 50}, 
}

STARTING_POSITIONS_DEFENSE = {
    "PG": {"x": 300, "y": 380},   
    "SG": {"x": 160, "y": 300},   
    "SF": {"x": 440, "y": 300},   
    "PF": {"x": 180, "y": 30},   
    "C":  {"x": 400, "y": 30},    
}

# --- The Node Logic ---

def initial_setup_node(state: AgentState) -> Dict[str, Any]:
    """
    1. Loads teams from the CSV-based Roster.
    2. Selects Top 5 players by Minutes Played (MP).
    3. Positions them on the court.
    4. Gives the ball to the Offensive Point Guard (PG).
    """
    user_team_abbr = state.get("user_team")
    opp_team_abbr = state.get("opponent_team")
    
    # Validation
    if not user_team_abbr or not opp_team_abbr:
        return {
            "messages": [AIMessage(content="Please specify your team and the opponent to start.")]
        }

    # 1. Fetch Rosters (using our updated logic)
    user_roster = get_team_roster(user_team_abbr)
    opp_roster = get_team_roster(opp_team_abbr)

    if not user_roster:
        return {"messages": [AIMessage(content=f"Error: Could not load roster for {user_team_abbr}. Check CSV.")]}

    # 2. Select Starters: Sort by MP (Minutes Played) descending and take top 5
    # This ensures we get the real starters like LeBron, Luka, etc.
    user_starters = sorted(user_roster, key=lambda x: x['stats']['mp'], reverse=True)[:5]
    opp_starters = sorted(opp_roster, key=lambda x: x['stats']['mp'], reverse=True)[:5]

    all_players_on_board = []
    
    # We map the sorted players to positions based on simple index for now.
    # Ideally: Sort user_starters so the player with high AST is at PG index.
    # Heuristic: Re-sort starters so the one with most Assists is first (PG)
    user_starters.sort(key=lambda x: x['stats']['ast'], reverse=True)
    
    # Define position mapping order
    position_slots = ["PG", "SG", "SF", "PF", "C"]
    
    ball_init_pos = None
    ball_handler_id = None

    # 3. Place Offense (User Team)
    for i, player in enumerate(user_starters):
        # Safety check if we have fewer than 5 players
        slot = position_slots[i] if i < len(position_slots) else "Bench"
        coords = STARTING_POSITIONS_OFFENSE.get(slot, {"x": 0, "y": 0})
        
        # Determine if this player starts with the ball (The PG)
        if slot == "PG":
            ball_init_pos = coords
            ball_handler_id = player["id"]

        player_node = {
            "id": player["id"],
            "type": "playerNode", # Must match React Flow custom node type
            "position": coords,
            "data": {
                **player,           # Includes stats, skills, name
                "side": "ATTACK",   # Frontend uses this for color (Blue)
                "label": player["name"],
                "jersey": i + 1     # Optional visual
            }
        }
        all_players_on_board.append(player_node)

    # 4. Place Defense (Opponent Team)
    for i, player in enumerate(opp_starters):
        slot = position_slots[i] if i < len(position_slots) else "Bench"
        coords = STARTING_POSITIONS_DEFENSE.get(slot, {"x": 800, "y": 0})
        
        player_node = {
            "id": player["id"],
            "type": "playerNode",
            "position": coords,
            "data": {
                **player,
                "side": "DEFENSE", # Frontend uses this for color (Red)
                "label": player["name"],
                "jersey": i + 10
            }
        }
        all_players_on_board.append(player_node)

    # 5. Return updated state
    return {
        "players": all_players_on_board,
        "ball_position": ball_init_pos,   # The ball starts at the PG's xy
        "ball_handler_id": ball_handler_id, # The PG holds the ball
        "setup_complete": True,
        "messages": [
            AIMessage(content=f"Court initialized: {user_team_abbr} (Offense) vs {opp_team_abbr} (Defense). Ball is with {user_starters[0]['name']}.")
        ]
    }