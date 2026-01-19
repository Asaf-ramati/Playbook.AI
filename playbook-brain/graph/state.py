from typing import Annotated, List, Dict, Optional, Any
from langchain_core.messages import BaseMessage
from langgraph.graph import add_messages
from typing_extensions import TypedDict 

class AgentState(TypedDict):
    """
    The shared State for Python and React.
    """
    # --- Core fields ---
    messages: Annotated[List[BaseMessage], add_messages]

    # --- Game fields ---
    ball_position: Dict[str, float]
    user_team: Optional[str]
    opponent_team: Optional[str]
    setup_complete: bool
    players: List[dict]

    # --- Logic fields ---
    analysis: Optional[dict]
    selected_play: Optional[dict]
    current_step_index: Optional[int]

    # --- Navigation fields (fix here) ---
    should_analyze: Optional[bool]
    intent: Optional[str]
    route_to: Optional[str]  # <--- Add this line (required!)
    target_play: Optional[str]

    # --- Integrations ---
    copilotkit: Optional[dict]