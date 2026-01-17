from typing import Dict, Any, Literal, Optional
from pydantic import BaseModel, Field
from graph.state import AgentState
from coach.playbook import PLAYBOOK
from .llm_utils import get_llm
from graph.constants import get_team_abbreviation 

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
    current_user_team = state.get('user_team')
    current_opp_team = state.get('opponent_team')

    print(f"\n🎯 ROUTER NODE | Teams: {current_user_team} vs {current_opp_team}")

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
    1. **SETUP**: If the user mentions a team name (Lakers, Celtics, Warriors, etc.) OR if teams are NOT SET yet.
       - Extract the team names in natural language (e.g., "Lakers", "Boston", "Celtics")
       - Identify which team the user wants to coach and which is the opponent
       
    2. **CONSULT/PLAYBOOK/ADJUST**: Only use these if BOTH teams are already set.
    
    **Output:**
    - intent: "SETUP" if teams need configuration
    - user_team: The team name the user wants to coach (natural language, e.g., "Lakers")
    - opponent_team: The opponent team name (natural language, e.g., "Boston" or "Celtics")
    - reasoning: Brief explanation
    
    **Examples:**
    - "I'm the Lakers coach playing Boston" → user_team: "Lakers", opponent_team: "Boston"
    - "Let's do Warriors vs Celtics, I'm Golden State" → user_team: "Warriors", opponent_team: "Celtics"
    """
    
    decision = structured_llm.invoke(router_prompt)

    print(f"🤖 Intent: {decision.intent} | Extracted: {decision.user_team} vs {decision.opponent_team}")

    # Convert natural language team names to abbreviations
    final_user_team = current_user_team
    final_opp_team = current_opp_team

    if decision.user_team:
        try:
            final_user_team = get_team_abbreviation(decision.user_team)
            print(f"✅ '{decision.user_team}' → '{final_user_team}'")
        except ValueError:
            print(f"❌ Could not find abbreviation for '{decision.user_team}'")

    if decision.opponent_team:
        try:
            final_opp_team = get_team_abbreviation(decision.opponent_team)
            print(f"✅ '{decision.opponent_team}' → '{final_opp_team}'")
        except ValueError:
            print(f"❌ Could not find abbreviation for '{decision.opponent_team}'")

    print(f"➡️  Routing to: {decision.intent}\n")

    return {
        "intent": decision.intent,
        "target_play": decision.play_id,
        "user_team": final_user_team,
        "opponent_team": final_opp_team
    }