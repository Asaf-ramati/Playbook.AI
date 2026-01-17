from typing import Annotated, List, Dict, Optional, Any
from langchain_core.messages import BaseMessage
from langgraph.graph import add_messages
from typing_extensions import TypedDict 

class AgentState(TypedDict):
    """
    ה-State המשותף ל-Python ול-React.
    """
    # --- שדות ליבה ---
    messages: Annotated[List[BaseMessage], add_messages]
    
    # --- שדות משחק ---
    ball_position: Dict[str, float]
    user_team: Optional[str]
    opponent_team: Optional[str]
    setup_complete: bool
    players: List[dict] 
    
    # --- שדות לוגיקה ---
    analysis: Optional[dict]
    selected_play: Optional[dict]
    
    # --- שדות ניווט (התיקון כאן) ---
    should_analyze: Optional[bool] 
    intent: Optional[str]
    route_to: Optional[str]  # <--- הוסף את השורה הזו חובה!
    
    # --- אינטגרציות ---
    copilotkit: Optional[dict]