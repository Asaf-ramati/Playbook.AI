import time
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
    
    # State variables
    current_ball_handler = state.get("ball_handler_id")
    current_ball_pos = state.get("ball_position")
    current_step_index = state.get("current_step_index", 0)
    
    updates_map = {} 
    new_ball_handler = current_ball_handler 
    
    # משתני ברירת מחדל לערכי החזרה
    action_description = ""
    next_step_index = 0
    final_intent = None # ברירת מחדל: מסיים את הפעולה

    # ---------------------------------------------------------
    # Case A: Execute a Pre-defined Play (Step-by-Step)
    # ---------------------------------------------------------
    if intent in ["PLAYBOOK", "AWAITING_ANIMATION"]:
        play = state.get("selected_play")
        
        if play and "steps" in play:
            total_steps = len(play["steps"])
            
            # Check if we have steps left to execute
            if current_step_index < total_steps:
                step_data = play["steps"][current_step_index]
                
                # 1. Map Roles to Real IDs
                role_to_real_id = _map_roles_to_ids(current_players)
                ball_pos_in_step = None

                # 2. Calculate Moves for this Step
                for item in step_data:
                    role_id = item.get("id") 
                    target_pos = {"x": item["x"], "y": item["y"]}

                    if role_id == "ball":
                        current_ball_pos = target_pos
                        ball_pos_in_step = target_pos
                    else:
                        real_id = role_to_real_id.get(role_id)
                        if real_id:
                            updates_map[real_id] = target_pos

                # 3. Determine New Ball Handler
                if ball_pos_in_step:
                    handler_found_in_step = False
                    for real_id, pos in updates_map.items():
                        if (pos["x"] == ball_pos_in_step["x"] and 
                            pos["y"] == ball_pos_in_step["y"]):
                            new_ball_handler = real_id
                            handler_found_in_step = True
                            break

                # --- לוגיקת חישוב הצעד הבא (תוקנה) ---
                calc_next_index = current_step_index + 1
                
                # אם סיימנו את כל הצעדים
                if calc_next_index >= total_steps:
                    next_step_index = 0 # איפוס לפעם הבאה
                    final_intent = None # סיום התהליך בגרף
                    action_description = f"Play '{play['name']}' Complete."
                else:
                    next_step_index = calc_next_index
                    # כאן אנחנו משתמשים בשיטת ה-Handshake:
                    # אנחנו שולחים סטטוס מיוחד שממתין ל-Frontend
                    final_intent = "AWAITING_ANIMATION" 
                    action_description = f"Executing Step {current_step_index + 1}/{total_steps}..."
                    time.sleep(2.5)
                    
            else:
                action_description = "Play already completed."
                next_step_index = 0
                final_intent = None
        else:
            return {"messages": [AIMessage(content="Error: Play execution failed (No steps found).")]}

    # ---------------------------------------------------------
    # Case B: Manual Adjustment
    # ---------------------------------------------------------
    elif intent == "ADJUST":
        llm = get_llm()
        user_command = state["messages"][-1].content
        
        player_list_str = "\n".join([f"- {p['id']} ({p['data']['name']})" for p in current_players])
        
        adjust_prompt = f"""
        You are a Motion Physics Engine. Translate command to coordinates.
        **Players:** {player_list_str}
        **Court Key:** Top(400,400), Paint(400,100), LeftCorner(50,50), RightCorner(750,50).
        **Command:** "{user_command}"
        Return list of moves.
        """
        
        structured_llm = llm.with_structured_output(AdjustmentOutput)
        result = structured_llm.invoke(adjust_prompt)
        
        for move in result.moves:
            updates_map[move.player_id] = {"x": move.x, "y": move.y}
            
        action_description = "Manual adjustment executed."
        final_intent = None # סיום פעולה ידנית

    # ---------------------------------------------------------
    # Case C: Pass the Ball
    # ---------------------------------------------------------
    elif intent == "PASS":
        llm = get_llm()
        user_command = state["messages"][-1].content
        
        # רשימת השחקנים לצורך זיהוי שמות
        player_list_str = "\n".join([f"- {p['id']} ({p['data']['name']})" for p in current_players if p['data']['side'] == 'ATTACK'])
        
        pass_prompt = f"""
        You are the Ball Controller. Identify the target player for the pass.

        **Offense Players:**
        {player_list_str}

        **Command:** "{user_command}"

        **IMPORTANT:** Return ONLY the player ID (e.g., "lal-lebron-james"), nothing else.
        Do NOT return the player name, do NOT add any explanation.

        Player ID:
        """
        
        target_player_id = llm.invoke(pass_prompt).content.strip()
        
        # מציאת השחקן במערך הנוכחי כדי לקבל את המיקום שלו
        target_player = next((p for p in current_players if p['id'] == target_player_id), None)
        
        if target_player:
            new_ball_handler = target_player_id
            current_ball_pos = target_player["position"]
            action_description = f"Pass complete to {target_player['data']['name']}."
        else:
            action_description = "Pass failed: Target player not found."

    # ---------------------------------------------------------
    # Apply Updates to State (Unified Logic)
    # ---------------------------------------------------------
    
    updated_players_list = []
    final_ball_pos = current_ball_pos
    
    # 1. נמצא קודם את השחקן שאמור להחזיק בכדור
    target_handler = next((p for p in current_players if p["id"] == new_ball_handler), None)
    
    # 2. בדיקת בטיחות: האם הוא שחקן התקפה?
    # אם הוא לא מהתקפה, נשאיר את המחזיק הקודם או נבטל את ההחזקה
    if target_handler and target_handler.get("data", {}).get("side") != "ATTACK":
        print(f"⚠️ Blocked ball transfer to defender: {new_ball_handler}")
        new_ball_handler = current_ball_handler # מחזירים למחזיק המקורי
    
    # 3. עדכון המיקומים
    for player in current_players:
        p_id = player["id"]
        new_props = player.copy()
        
        # עדכון מיקום שחקן
        if p_id in updates_map:
            new_props["position"] = updates_map[p_id]
        
        # הצמדת הכדור לידיים של שחקן ההתקפה בלבד
        if p_id == new_ball_handler:
            # הכדור תמיד יקבל את המיקום של המחזיק (התקפה בלבד)
            final_ball_pos = new_props["position"]
            
        updated_players_list.append(new_props)
    
    return {
        "players": updated_players_list,
        "ball_position": final_ball_pos,
        "ball_handler_id": new_ball_handler,
        "current_step_index": next_step_index,
        "intent": final_intent,
        "messages": [AIMessage(content=action_description)]
    }