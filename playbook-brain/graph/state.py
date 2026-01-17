from typing import Annotated, List, TypedDict, Optional
from langchain_core.messages import BaseMessage
from langgraph.graph import add_messages

class AgentState(TypedDict):
    """State המשותף לכל הגרף"""
    messages: Annotated[List[BaseMessage], add_messages]
    copilotkit: Optional[dict]  # מידע מה-Frontend
    analysis: Optional[dict]  # תוצאות הניתוח
    selected_play: Optional[dict]  # המהלך שנבחר