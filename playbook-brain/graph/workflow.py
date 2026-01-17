from langgraph.graph import StateGraph, START, END
from .state import AgentState
from .nodes import (
    analyzer_node, 
    router_node, 
    consultant_node, 
    playbook_selector_node, 
    executor_node
)

def route_next_step(state: AgentState):
    """
    Determines the next node based on the Router's decision.
    """
    intent = state.get("intent")
    
    if intent == "CONSULT":
        return "consultant"      # Go to the "Mouth" (Text advice only)
    elif intent == "PLAYBOOK":
        return "playbook_selector" # Go to the "Librarian" (Fetch play data)
    elif intent == "ADJUST":
        return "executor"        # Go directly to "Hands" (Manual movement)
        
    return "consultant" # Default fallback

def create_graph():
    workflow = StateGraph(AgentState)
    
    # --- Add Nodes ---
    workflow.add_node("analyzer", analyzer_node)
    workflow.add_node("router", router_node)
    workflow.add_node("consultant", consultant_node)
    workflow.add_node("playbook_selector", playbook_selector_node)
    workflow.add_node("executor", executor_node)
    
    # --- Define Flow ---
    
    # 1. Start with Analysis
    workflow.add_edge(START, "analyzer")
    
    # 2. Move to Decision Making
    workflow.add_edge("analyzer", "router")
    
    # 3. Conditional Routing (The "Split")
    workflow.add_conditional_edges(
        "router",
        route_next_step,
        {
            "consultant": "consultant",
            "playbook_selector": "playbook_selector",
            "executor": "executor"
        }
    )
    
    # 4. Closing the Loops
    # Playbook always flows to Executor to apply the changes
    workflow.add_edge("playbook_selector", "executor")
    
    # End states
    workflow.add_edge("consultant", END)
    workflow.add_edge("executor", END)
    
    return workflow.compile()

# Export the compiled graph
graph = create_graph()