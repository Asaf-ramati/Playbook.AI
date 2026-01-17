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
    Creates a map like: {'PG': 'lal-lebron-james', 'C': 'lal-anthony-davis'}
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
    """
    intent = state.get("intent")
    current_players = state.get("players", [])
    
    # State variables for the ball
    current_ball_handler = state.get("ball_handler_id")
    current_ball_pos = state.get("ball_position")
    current_step_index = state.get("current_step_index", 0)
    
    updates_map = {} # Stores target positions: {REAL_PLAYER_ID: {x, y}}
    new_ball_handler = current_ball_handler 
    
    action_description = ""
    next_step_index = 0
    is_play_active = False # Flag to determine if we are in the middle of a play

    # ---------------------------------------------------------
    # Case A: Execute a Pre-defined Play (Step-by-Step)
    # ---------------------------------------------------------
    if intent == "PLAYBOOK":
        play = state.get("selected_play")
        
        if play and "steps" in play:
            total_steps = len(play["steps"])
            
            # Check if we have steps left to execute
            if current_step_index < total_steps:
                is_play_active = True
                step_data = play["steps"][current_step_index]
                
                # --- 1. Map Roles to Real IDs ---
                # This is CRITICAL. It converts 'PG' -> 'lal-lebron-james'
                role_to_real_id = _map_roles_to_ids(current_players)
                
                ball_pos_in_step = None

                # --- 2. Calculate Moves for this Step ---
                for item in step_data:
                    role_id = item.get("id") # This is 'PG', 'C', or 'ball'
                    target_pos = {"x": item["x"], "y": item["y"]}

                    if role_id == "ball":
                        current_ball_pos = target_pos
                        ball_pos_in_step = target_pos
                    else:
                        # Find the real player ID for this role
                        real_id = role_to_real_id.get(role_id)
                        if real_id:
                            updates_map[real_id] = target_pos

                # --- 3. Determine New Ball Handler ---
                # If a player moves to the exact location of the ball, they take it.
                if ball_pos_in_step:
                    # Reset handler check
                    handler_found_in_step = False
                    
                    # Check moving players
                    for real_id, pos in updates_map.items():
                        if (pos["x"] == ball_pos_in_step["x"] and 
                            pos["y"] == ball_pos_in_step["y"]):
                            new_ball_handler = real_id
                            handler_found_in_step = True
                            break
                    
                    # If ball moved but no specific player grabbed it, it might be a pass
                    # If ball didn't move much, keep old handler.
                    # Simple logic: If no one is at ball pos, handler is None (pass in air)
                    if not handler_found_in_step:
                         # Optional: Check if ball is still with old handler? 
                         # For now, if ball moves away from handler, handler loses it.
                         pass 

                # Prepare index for next turn
                next_step_index = current_step_index + 1
                
                if next_step_index < total_steps:
                    action_description = f"Running {play['name']}: Step {current_step_index + 1}/{total_steps} executed."
                else:
                    action_description = f"Running {play['name']}: Final Step Completed."
                    # Reset for next play
                    next_step_index = 0
                    is_play_active = False 

            else:
                action_description = "Play already completed."
                next_step_index = 0
                
        else:
            return {"messages": [AIMessage(content="Error: Play execution failed (No steps found).")]}

    # ---------------------------------------------------------
    # Case B: Manual Adjustment (Natural Language)
    # ---------------------------------------------------------
    elif intent == "ADJUST":
        llm = get_llm()
        user_command = state["messages"][-1].content
        
        # Context for the LLM
        player_list_str = "\n".join([f"- {p['id']} ({p['data']['name']})" for p in current_players])
        
        adjust_prompt = f"""
        You are a Motion Physics Engine. Translate command to coordinates.
        
        **Players:**
        {player_list_str}
        
        **Court Key:** Top(400,400), Paint(400,100), LeftCorner(50,50), RightCorner(750,50).
        
        **Command:** "{user_command}"
        
        Return list of moves.
        """
        
        structured_llm = llm.with_structured_output(AdjustmentOutput)
        result = structured_llm.invoke(adjust_prompt)
        
        for move in result.moves:
            updates_map[move.player_id] = {"x": move.x, "y": move.y}
            
        action_description = "Manual adjustment executed."

    # ---------------------------------------------------------
    # Apply Updates to State (Unified Logic)
    # ---------------------------------------------------------
    
    updated_players_list = []
    final_ball_pos = current_ball_pos
    
    for player in current_players:
        p_id = player["id"]
        new_props = player.copy()
        
        # 1. Update Position if this player moved
        if p_id in updates_map:
            new_props["position"] = updates_map[p_id]
        
        # 2. Sticky Ball Physics
        # If this player is the Ball Handler, ensure the ball is attached to them
        # (This overrides independent ball movement if a handler is defined)
        if p_id == new_ball_handler:
            final_ball_pos = new_props["position"]
            
        updated_players_list.append(new_props)

    # Decide on Intent: 
    # If play is still running (multi-step), keep intent as PLAYBOOK so graph loops or waits.
    # If play is done, set intent to None or wait for user input.
    final_intent = "PLAYBOOK" if is_play_active else None

    return {
        "players": updated_players_list,
        "ball_position": final_ball_pos,
        "ball_handler_id": new_ball_handler,
        "current_step_index": next_step_index,
        "intent": final_intent, 
        "messages": [AIMessage(content=action_description)]
    }