from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage
from .state import AgentState
import os
from typing import Dict, Any

def get_llm():
    """Lazy load the LLM to ensure env vars are loaded first"""
    return ChatOpenAI(model="gpt-4o", api_key=os.getenv("OPENAI_API_KEY"))

def analyzer_node(state: AgentState) -> Dict[str, Any]:
    """מנתח את מצב המגרש ומחזיר ניתוח"""
    llm = get_llm()

    # קבל את הקונטקסט
    context = state.get("copilotkit", {}).get("context", [])

    # מצא את הקונטקסט של עמדות השחקנים
    positions_context = None
    for ctx in context:
        if "positions" in ctx.get("description", "").lower():
            positions_context = ctx.get("value", "")
            break

    # בנה prompt לניתוח
    analysis_prompt = f"""
    אתה מאמן כדורסל מקצועי. נתח את מצב המגרש הנוכחי.

    עמדות השחקנים: {positions_context}

    תן ציון spacing (0-10) והמלצות טקטיות קצרות.
    """

    response = llm.invoke([{"role": "user", "content": analysis_prompt}])

    return {
        "messages": [AIMessage(content=f"Coach Analysis: {response.content}")],
        "analysis": {
            "spacing_score": 7,
            "clogged_areas": [],
            "tactical_summary": response.content
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
        return {"messages": [AIMessage(content="No play selected to execute.")]}

    movements = selected_play.get("positions", [])
    play_name = selected_play.get("name", "Unknown Play")

    # פשוט החזר הודעה עם המידע
    return {
        "messages": [AIMessage(
            content=f"מבצע את המהלך: {play_name}. עמדות: {movements}"
        )],
        "selected_play": selected_play  # שמור ב-state
    }