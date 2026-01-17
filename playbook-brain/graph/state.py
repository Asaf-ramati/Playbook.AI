from typing import Annotated, List, TypedDict, Optional, Dict
from langchain_core.messages import BaseMessage
from langgraph.graph import add_messages
# שימוש ב-typing_extensions עבור גרסאות פייתון < 3.12 כפי שהשרת המליץ
from typing_extensions import TypedDict 

class AgentState(TypedDict):
    """
    ה-State המשותף ל-Python ול-React.
    כל שינוי כאן יתעדכן אוטומטית ב-Frontend בזכות useCoAgent.
    """
    ball_position: Dict[str, float]
    user_team: str
    opponent_team: str
    setup_complete: bool
    messages: Annotated[List[BaseMessage], add_messages]
    players: List[dict] 
    analysis: Optional[dict]
    selected_play: Optional[dict]
    copilotkit: Optional[dict]