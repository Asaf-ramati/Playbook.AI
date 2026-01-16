from langchain_openai import ChatOpenAI
from .state import AgentState
from coach.playbook import PLAYBOOK

llm = ChatOpenAI(model="gpt-4o")

def analyzer_node(state: AgentState):
    positions = state.get("player_positions", [])
    return {"analysis": f"המגרש מנותח. נמצאו {len(positions)} שחקנים."}

def strategist_node(state: AgentState):
    play = PLAYBOOK["BASIC_SPACING"]
    return {"selected_play": play}

def executor_node(state: AgentState):
    return state