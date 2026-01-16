from typing import Annotated, List, TypedDict
from langchain_core.messages import BaseMessage

class AgentState(TypedDict):
    messages: List[BaseMessage]
    player_positions: List[dict]
    analysis: str
    selected_play: dict
    current_step: int