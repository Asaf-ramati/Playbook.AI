from typing import Dict, Any, List
from langchain_core.messages import AIMessage
from pydantic import BaseModel, Field
from graph.state import AgentState
from .llm_utils import get_llm


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