from typing import Dict, Any, Literal, Optional
from pydantic import BaseModel, Field
from graph.state import AgentState
from coach.playbook import PLAYBOOK
from .llm_utils import get_llm

class RouterDecision(BaseModel):
    """
    Decision structure including SETUP for NBA team selection.
    """
    intent: Literal["CONSULT", "PLAYBOOK", "ADJUST", "SETUP"] = Field(
        ...,
        description="CONSULT: advice, PLAYBOOK: run play, ADJUST: manual move, SETUP: selecting NBA teams."
    )
    play_id: Optional[str] = Field(None)
    user_team: Optional[str] = Field(None, description="The team the user selected (e.g., 'LAL')")
    opponent_team: Optional[str] = Field(None, description="The opponent team selected (e.g., 'BOS')")
    reasoning: str = Field(...)

def router_node(state: AgentState) -> Dict[str, Any]:
    llm = get_llm()
    structured_llm = llm.with_structured_output(RouterDecision)
    
    user_message = state['messages'][-1].content
    # Check if teams are already set in state
    current_user_team = state.get('user_team')
    current_opp_team = state.get('opponent_team')
    
    tactical_summary = state.get('analysis', {}).get('tactical_summary', 'No analysis available')
    available_plays_str = ", ".join(PLAYBOOK.keys())
    
    router_prompt = f"""
    You are the NBA Head Coach Logic Unit.
    
    **Current Game Config:**
    - User Team: {current_user_team if current_user_team else "NOT SET"}
    - Opponent: {current_opp_team if current_opp_team else "NOT SET"}

    **Context:**
    1. User Message: "{user_message}"
    2. Court Analysis: {tactical_summary}
    3. Plays: [{available_plays_str}]

    **Decision Logic:**
    1. **SETUP**: If the user mentions a team name (Lakers, BOS, NYK, etc.) OR if teams are NOT SET yet.
       - Your goal is to identify which team the user wants to be and who they play against.
    2. **CONSULT/PLAYBOOK/ADJUST**: Only use these if BOTH teams are already set.
    
    **Output:**
    Identify the intent. If SETUP, try to extract the team abbreviations (e.g., 'LAL', 'BOS', 'GSW').
    """
    
    decision = structured_llm.invoke(router_prompt)
    
    # Update state logic
    return {
        "intent": decision.intent,
        "target_play": decision.play_id,
        "user_team": decision.user_team or current_user_team,
        "opponent_team": decision.opponent_team or current_opp_team
    }