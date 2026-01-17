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

def analyzer_node(state: AgentState) -> Dict[str, Any]:
    """
    מנתח את המגרש בשתי שכבות:
    1. שכבה דטרמיניסטית (גיאומטריה + נתוני שחקנים).
    2. שכבה אסטרטגית (LLM שמבין את המשמעות).
    """
    raw_players = state.get('players', [])
    
    # שלב א': טעינת הסגלים (כדי לדעת מי זה מי)
    # הערה: בפרודקשן נדע איזה קבוצות משחקות לפי ה-State, כרגע נטען את ה-Mock
    lakers_roster = get_team_roster("lakers_mock")
    warriors_roster = get_team_roster("warriors_mock")
    full_roster = lakers_roster + warriors_roster
    
    # שלב ב': חישוב מדדים גיאומטריים (Spacing)
    spacing_data = analyze_spacing(raw_players)
    
    # שלב ג': בניית תמונת מצב מועשרת (Enriched Context)
    tactical_snapshot = []
    
    for p in raw_players:
        # 1. זיהוי מיקום גיאומטרי (איפה הוא עומד?)
        zone = identify_zone(p['position'])
        
        # 2. שליפת פרופיל שחקן (מי זה ומה הוא יודע לעשות?)
        profile = get_player_by_id(p['id'], full_roster)
        
        if profile:
            # בדיקת התאמה בין מיקום ליכולת (למשל: סנטר שעומד בשלוש)
            is_in_range = zone in profile['shooting_ranges'] or \
                          (zone == "TOP_3" and "3pt" in profile['shooting_ranges'])
            
            position_note = "Effective Range" if is_in_range else "OUT OF POSITION"
            
            info = (
                f"- {profile['name']} ({profile['position']}) | "
                f"Loc: {zone} | Role: {profile['archetype']} | "
                f"Status: {position_note}"
            )
        else:
            # Fallback לשחקן לא מוכר
            info = f"- Unknown Player ({p['id']}) at {zone}"
            
        tactical_snapshot.append(info)

    snapshot_text = "\n".join(tactical_snapshot)

    # שלב ד': ניתוח ה-LLM (ה"מוח")
    # אנחנו שואלים אותו שאלות שיתאימו גם לייעוץ וגם לפעולה
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
    
    # הדפסה ללוג כדי שנראה מה הוא "רואה"
    print(f"--- ANALYZER OUTPUT ---\n{response.content}\n-----------------------")

    # החזרת הנתונים ל-State כדי שה-Router וה-Strategist ישתמשו בהם
    return {
        # שומרים את ההודעה האחרונה מהמשתמש (לא דורסים) + מוסיפים לוג פנימי אם רוצים
        # אבל כאן ה-Graph מצפה לעדכון מפתחות
        "analysis": {
            "spacing_score": spacing_data['score'],
            "is_clogged": spacing_data['is_clogged'],
            "tactical_summary": response.content,
            "snapshot_text": snapshot_text # שומרים את הטקסט הגולמי לשימוש ה-Consultant
        }
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