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
    intent: Literal["CONSULT", "PLAYBOOK", "ADJUST", "SETUP", "PASS", "GENERATE"] = Field(
        ...,
        description="The categorization of the user's request."
    )
    play_id: Optional[str] = Field(None, description="The EXACT ID of the play from the Available Plays list (if intent is PLAYBOOK)")
    user_team: Optional[str] = Field(None, description="Only if changing teams: The new user team")
    opponent_team: Optional[str] = Field(None, description="Only if changing teams: The new opponent team")
    reasoning: str = Field(...)

def router_node(state: AgentState) -> Dict[str, Any]:

    llm = get_llm()
    structured_llm = llm.with_structured_output(RouterDecision)

    user_message = state['messages'][-1].content
    current_user_team = state.get('user_team')
    current_opp_team = state.get('opponent_team')

    print(f"\n🎯 ROUTER NODE | Current State: {current_user_team} vs {current_opp_team}")

    if "pass" in user_message.lower():
        print("🏀 PASS detected!")
        return {"intent": "PASS"}

    # Generate a formatted list of plays with descriptions for better context
    play_descriptions = "\n".join([f"- {pid}: {data['name']} ({data['description']})" for pid, data in PLAYBOOK.items()])

    router_prompt = f"""
    You are the Brain of an NBA Coaching Assistant. determine the NEXT STEP based on the user's request.

    **CURRENT CONTEXT:**
    - Teams Configured: {bool(current_user_team)} ({current_user_team} vs {current_opp_team})
    - User Request: "{user_message}"

    **AVAILABLE PLAYS (ID: Name - Description):**
    {play_descriptions}

    **DECISION LOGIC (Order of Importance):**

    1. **SETUP** (Initialization & Reset):
       - CHOOSE THIS IF:
         a) Teams are NOT set yet (Current is None).
         b) User EXPLICITLY asks to CHANGE teams (e.g., "Switch to Celtics").
         c) User wants to RESET the court or START OVER (e.g., "Reset", "Put everyone back to start", "Organise the players like in the beginning", "Clear the court").
       - ACTION: 
         * For Team Changes: Extract `user_team` and `opponent_team`.
         * For Resets: Keep current teams but set a flag (like `intent: SETUP`) to trigger the reset logic.

    2. **PLAYBOOK** (Running Tactics):
       - CHOOSE THIS IF:
         a) Teams ARE set.
         b) User asks to run a play that is look familiar from the playbook, or specific movement.
       - ACTION: You MUST map the request to the closest `play_id` from the AVAILABLE PLAYS list.
         * (PNR, Horns, etc. - keep your existing list here)
    
    3. **GENERATE** (Custom Movements):  
   - CHOOSE THIS IF:
     a) Teams ARE set.
     b) User asks for specific player movements that DON'T match any play.
     c) Examples: "Move LeBron to the post", "Send AD to the corner"

    4. **ADJUST** (Manual Changes):
       - CHOOSE THIS IF: User wants to move a specific player manually (e.g., "Move LeBron to the corner").

    5. **CONSULT** (Strategic Advice):
       - CHOOSE THIS IF: 
         a) User asks "what", "how", "why" questions.
         b) Greetings or general conversation.

    **OUTPUT INSTRUCTIONS:**
    - If intent is SETUP and it's a RESET request, return `intent: SETUP` and reuse current team names.
    - If intent is PLAYBOOK, you MUST fill `play_id` with the EXACT string from the list above.
    """

    decision = structured_llm.invoke(router_prompt)

    print(f"🤖 Intent: {decision.intent} | Play: {decision.play_id} | Teams: {decision.user_team} vs {decision.opponent_team}")

    # Handle Team Name Normalization for SETUP
    final_user_team = current_user_team
    final_opp_team = current_opp_team

    if decision.intent == "SETUP":
        if decision.user_team:
            try:
                final_user_team = get_team_abbreviation(decision.user_team)
            except ValueError:
                pass
        if decision.opponent_team:
            try:
                final_opp_team = get_team_abbreviation(decision.opponent_team)
            except ValueError:
                pass

    # Handle Play Selection
    selected_play_data = None
    if decision.intent == "PLAYBOOK" and decision.play_id:
        selected_play_data = PLAYBOOK.get(decision.play_id)

    return {
        "intent": decision.intent,
        "selected_play": selected_play_data, # Stores the play data in State
        "user_team": final_user_team,
        "opponent_team": final_opp_team,
        "target_play": decision.play_id # Ensure this matches what playbook_selector expects
    }