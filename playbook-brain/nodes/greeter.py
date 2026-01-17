from typing import Dict, Any, Literal
from pydantic import BaseModel, Field
from langchain_core.messages import AIMessage
from graph.state import AgentState
from .llm_utils import get_llm


class GreeterDecision(BaseModel):
    """
    Determines if the user message is casual conversation or basketball-related.
    """
    message_type: Literal["GREETING", "CASUAL", "BASKETBALL"] = Field(
        ...,
        description=(
            "GREETING: Hi/Hello/Hey type messages. "
            "CASUAL: General chat not about basketball. "
            "BASKETBALL: Tactical questions, team setup, or play requests."
        )
    )
    reasoning: str = Field(..., description="Brief explanation of the classification")


def greeter_node(state: AgentState) -> Dict[str, Any]:
    """
    The 'Greeter' - First line of defense.
    
    Purpose:
    - Handles casual conversation (greetings, small talk)
    - Routes basketball-related queries to the analyzer
    - Prevents unnecessary tactical analysis for simple messages
    
    Flow:
    - If GREETING/CASUAL: Responds directly and marks should_analyze=False
    - If BASKETBALL: Passes through to analyzer (should_analyze=True)
    """
    llm = get_llm()
    structured_llm = llm.with_structured_output(GreeterDecision)
    
    # Get the latest user message
    user_message = state['messages'][-1].content
    
    # Check current setup status
    setup_complete = state.get('setup_complete', False)
    user_team = state.get('user_team')
    opponent_team = state.get('opponent_team')
    
    # Classification prompt
    classification_prompt = f"""
    You are a message classifier for an NBA coaching AI assistant.
    
    **Current Context:**
    - Setup Complete: {setup_complete}
    - Teams Selected: {user_team} vs {opponent_team if opponent_team else "None"}
    
    **User Message:**
    "{user_message}"
    
    **Classification Rules:**
    1. **GREETING**: Simple greetings like "hi", "hello", "hey", "what's up"
    2. **CASUAL**: General conversation not related to basketball tactics
    3. **BASKETBALL**: Any of the following:
       - Team selection (Lakers, Warriors, etc.)
       - Tactical questions (spacing, plays, positioning)
       - Play execution requests
       - Player movement instructions
       - Strategy discussions
    
    Classify this message.
    """
    
    decision = structured_llm.invoke(classification_prompt)
    
    print(f"🤖 LLM Classification: {decision.message_type}")
    print(f"💭 Reasoning: {decision.reasoning}")

    # Handle based on classification
    if decision.message_type in ["GREETING", "CASUAL"]:
        print(f"➡️  ROUTING TO: end (casual conversation)")
        # Generate a friendly response without tactical analysis
        response_prompt = f"""
        You are a friendly NBA Head Coach AI assistant.
        
        **User said:** "{user_message}"
        
        **Context:**
        - Setup Status: {"Game ready" if setup_complete else "No teams selected yet"}
        - Current Matchup: {f"{user_team} vs {opponent_team}" if user_team and opponent_team else "Not set"}
        
        **Instructions:**
        1. Respond warmly and professionally
        2. If it's a greeting and no teams are set, briefly mention they can select teams to start
        3. If teams are already set, acknowledge the current game
        4. Keep it conversational and brief (1-2 sentences)
        5. Don't provide tactical analysis unless asked
        
        Examples:
        - "Hey!" → "Hey there, Coach! Ready to break down some plays? Just let me know which teams you want to work with."
        - "How are you?" → "I'm doing great! Currently analyzing the {user_team} vs {opponent_team} matchup. What would you like to focus on?"
        
        Respond now:
        """
        
        response = llm.invoke([{"role": "user", "content": response_prompt}])
        
        return {
            "messages": [AIMessage(content=response.content)],
            "should_analyze": False,  # Skip the analyzer
            "intent": "CASUAL"  # Mark as casual conversation
        }
    
    else: 
        # Check if this is a team setup message
        user_message_lower = user_message.lower()
        is_team_setup = any(keyword in user_message_lower for keyword in [
            "lakers", "celtics", "warriors", "heat", "bucks", "vs", "against", 
            "playing", "coach of", "head coach"
        ])
        
       
        if is_team_setup and not state.get('setup_complete', False):
            # Skip analyzer, go straight to router for team setup
            return {
                "should_analyze": False,
                "route_to": "router"  # New field to indicate where to go
            }
        else:
            # Normal basketball query - analyze first
            return {
                "should_analyze": True
            }