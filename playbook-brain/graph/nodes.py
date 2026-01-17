from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage
from .state import AgentState
import os
from typing import Dict, Any

def get_llm():
    """Lazy load the LLM to ensure env vars are loaded first"""
    return ChatOpenAI(model="gpt-4o", api_key=os.getenv("OPENAI_API_KEY"))


def analyzer_node(state: AgentState) -> Dict[str, Any]:
    """
    Analyzes the current court situation and player positions.
    Returns tactical insights and spacing analysis.
    """
    # Get player positions from state
    players = state.get('players', [])
    
    # Debug logging
    print(f"--- ANALYZER: Received {len(players)} players ---")
    for player in players:
        player_id = player.get('id', 'unknown')
        position = player.get('position', {})
        x = position.get('x', 0)
        y = position.get('y', 0)
        print(f"  Player {player_id} at ({x}, {y})")
    
    # Build a formatted string of player positions for the LLM
    positions_text = ""
    team1_players = []
    team2_players = []
    
    for player in players:
        player_id = player.get('id', '')
        player_data = player.get('data', {})
        position = player.get('position', {})
        
        name = player_data.get('name', player_id)
        pos = player_data.get('position', 'N/A')
        team = player_data.get('team', 'Unknown')
        x = position.get('x', 0)
        y = position.get('y', 0)
        
        player_info = f"{name} ({pos}) at coordinates ({x}, {y})"
        
        if 'team1' in player_id:
            team1_players.append(player_info)
        elif 'team2' in player_id:
            team2_players.append(player_info)
    
    positions_text = "TEAM 1 (Lakers):\n"
    positions_text += "\n".join(f"  - {p}" for p in team1_players)
    positions_text += "\n\nTEAM 2 (Warriors):\n"
    positions_text += "\n".join(f"  - {p}" for p in team2_players)
    
    # Create the analysis prompt
    analysis_prompt = f"""
You are a professional basketball coach analyzing the current court situation.

Current Player Positions:
{positions_text}

Please analyze:
1. Spacing quality (rate 0-10)
2. Identify any congested areas
3. Provide brief tactical recommendations

Keep your response concise and actionable.
"""
    
    # Get LLM and invoke
    llm = get_llm()
    response = llm.invoke([{"role": "user", "content": analysis_prompt}])
    
    # Parse the response to extract spacing score
    # Simple heuristic: look for a number in the response
    spacing_score = 7  # default
    content = response.content.lower()
    
    # Try to extract spacing score from response
    import re
    score_match = re.search(r'spacing.*?(\d+)', content)
    if score_match:
        try:
            spacing_score = int(score_match.group(1))
        except:
            pass
    
    # Return updated state
    return {
        "messages": [AIMessage(content=f"Court Analysis:\n{response.content}")],
        "analysis": {
            "spacing_score": spacing_score,
            "tactical_summary": response.content,
            "player_count": len(players)
        }
    }

def strategist_node(state: AgentState) -> Dict[str, Any]:
    """בוחר מהלך מתאים על בסיס הניתוח"""
    analysis = state.get("analysis", {})
    spacing_score = analysis.get("spacing_score", 5)

    play = {
    "name": "Basic Spacing",
    "description": "Position players in standard formation",
    "positions": []
    }

    return {
        "messages": [AIMessage(content=f"Spacing looks okay, but let's reinforce our basic structure.")],
        "selected_play": play
    }


def executor_node(state: AgentState) -> Dict[str, Any]:
    selected_play = state.get("selected_play")
    if not selected_play:
        return {"messages": [AIMessage(content="לא נבחר מהלך לביצוע.")]}

    # דוגמה למהלך 'Pick and Roll' פשוט שמעדכן קואורדינטות
    # בגרסה מתקדמת, כאן תהיה לוגיקה שמחשבת x ו-y לכל שחקן
    updated_players = list(state["players"]) # העתקת המצב הקיים
    
    for player in updated_players:
        if player["id"] == "team1-pg": # רכז
            player["position"] = {"x": 400, "y": 300}
        elif player["id"] == "team1-c": # סנטר חוסם
            player["position"] = {"x": 420, "y": 320}

    return {
        "players": updated_players, # זה מה שיגרום למגרש ב-React לזוז מיד!
        "messages": [AIMessage(content=f"מבצע את המהלך: {selected_play['name']}. השחקנים זזים לעמדות.")]
    }