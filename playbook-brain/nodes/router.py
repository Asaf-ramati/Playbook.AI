from typing import Dict, Any, Literal, Optional
from pydantic import BaseModel, Field
from graph.state import AgentState
from coach.playbook import PLAYBOOK
from .llm_utils import get_llm


class RouterDecision(BaseModel):
    """
    Represents the strict decision structure the Router must return.
    This ensures the graph always knows exactly where to go next.
    """
    intent: Literal["CONSULT", "PLAYBOOK", "ADJUST"] = Field(
        ...,
        description="The determined intent: 'CONSULT' for advice/questions, 'PLAYBOOK' to run a set play, 'ADJUST' for manual commands."
    )
    play_id: Optional[str] = Field(
        None,
        description="If intent is PLAYBOOK, this MUST be one of the keys provided in the context. If no specific play matches, select the most tactical fit."
    )
    reasoning: str = Field(
        ...,
        description="A brief explanation of why this intent and play (if any) were chosen."
    )


def router_node(state: AgentState) -> Dict[str, Any]:
    """
    The Decision Unit.
    It takes the User's input and the Analyzer's insights to decide on the next step.
    It does NOT modify the players; it only routes the flow.
    """
    llm = get_llm()
    
    # Bind the Pydantic model to the LLM to force JSON output
    structured_llm = llm.with_structured_output(RouterDecision)
    
    # Prepare context for the prompt
    user_message = state['messages'][-1].content
    tactical_summary = state.get('analysis', {}).get('tactical_summary', 'No analysis available')
    
    # Inject available plays so the LLM knows what's possible
    # We replace underscores with spaces for better readability in the prompt
    available_plays_str = ", ".join(PLAYBOOK.keys())
    
    router_prompt = f"""
    You are the Head Coach Logic Unit. Your goal is to determine the user's intent.

    **Context:**
    1. User Message: "{user_message}"
    2. Court Tactical Analysis: {tactical_summary}
    3. Available Plays in Database: [{available_plays_str}]

    **Decision Logic:**
    
    A. **CONSULT**: Return this if the user asks a question, wants an opinion, asks "what if", or discusses strategy without asking to move players.
       - Example: "What do you think about the spacing?"
       - Example: "Who should take the last shot?"

    B. **PLAYBOOK**: Return this if the user wants to execute a play, run a set, or if the user asks for a solution that requires moving the team.
       - You MUST try to map the request to one of the 'Available Plays'.
       - If the user says "Run a play" without specifying, pick the best play ID based on the Court Tactical Analysis.
       - Example: "Run a Pick and Roll." -> intent: PLAYBOOK, play_id: "PICK_AND_ROLL_TOP"

    C. **ADJUST**: Return this if the user gives a specific, manual command to move specific players.
       - Example: "Move LeBron to the corner."
       - Example: "Push the defense back."

    **Output Requirement:**
    Return a valid JSON object matching the RouterDecision schema.
    """
    
    # Invoke the LLM
    decision = structured_llm.invoke(router_prompt)
    
    # Log the decision for debugging purposes
    print(f"--- ROUTER DECISION: {decision.intent} | Play: {decision.play_id} | Reason: {decision.reasoning} ---")
    
    # Update the state with the decision variables
    return {
        "intent": decision.intent,
        "target_play": decision.play_id
    }