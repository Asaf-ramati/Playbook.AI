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
        
        if play and "steps" in play:
            # We assume executing Step 1 (index 0) for this turn
            # Future: Add 'step_index' to state to handle multi-step plays
            step_data = play["steps"][0] 
            
            # Map abstract roles (PG, C) to real Player IDs
            role_to_id = _map_roles_to_ids(current_players)
            
            # 1. Update Player Positions
            for role, coords in step_data.get("positions", {}).items():
                real_id = role_to_id.get(role)
                if real_id:
                    updates_map[real_id] = coords

            # 2. Check for Pass (Ball Movement)
            # If the step says "ball_handler": "C", we pass to the Center
            target_role = step_data.get("ball_handler")
            if target_role and target_role in role_to_id:
                new_ball_handler = role_to_id[target_role]
                action_description = f"Running {play['name']}: Passing to {target_role}."
            else:
                action_description = f"Running {play['name']}: Movement only."
                
        else:
            return {"messages": [AIMessage(content="Error: Play execution failed.")]}

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