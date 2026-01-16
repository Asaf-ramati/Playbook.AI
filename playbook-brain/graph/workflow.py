from langgraph.graph import StateGraph, START, END
from .state import AgentState
from .nodes import analyzer_node, strategist_node, executor_node

def create_graph():
    workflow = StateGraph(AgentState)
    
    workflow.add_node("analyzer", analyzer_node)
    workflow.add_node("strategist", strategist_node)
    workflow.add_node("executor", executor_node)
    
    workflow.add_edge(START, "analyzer")
    workflow.add_edge("analyzer", "strategist")
    workflow.add_edge("strategist", "executor")
    workflow.add_edge("executor", END)
    
    return workflow.compile()