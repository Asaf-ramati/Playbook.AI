from langgraph.graph import StateGraph, START, END
from graph.state import AgentState
from nodes import (
    analyzer_node,
    router_node,
    consultant_node,
    playbook_selector_node,
    executor_node,
    initial_setup_node,
    greeter_node  # ADD THIS
)

def should_analyze(state: AgentState):
    """
    Determines the next step after greeter.
    """
    if state.get("route_to") == "router":
        return "router"  # Skip analyzer, go to router
    elif state.get("should_analyze", True):
        return "analyzer"
    else:
        return "end"

def route_next_step(state: AgentState):
    """
    Determines the next node based on the Router's decision.
    """
    intent = state.get("intent")
    
    if intent == "SETUP":
        return "setup"
    elif intent == "CONSULT":
        return "consultant"
    elif intent == "PLAYBOOK":
        return "playbook_selector"
    elif intent == "ADJUST":
        return "executor"
        
    return "consultant"

def should_continue_play(state: AgentState):
    """
    בדוק אם יש עוד צעדים בתרגיל.
    אם intent=PLAYBOOK ויש current_step_index > 0, המשך לצעד הבא.
    """
    intent = state.get("intent")
    step_index = state.get("current_step_index", 0)
    
    # Continue if we're in playbook mode OR waiting for animation
    if intent in ["PLAYBOOK", "AWAITING_ANIMATION"] and step_index > 0:
        return "executor"  # ✅ Continue to next step
    else:
        return "end"

def create_graph():
    workflow = StateGraph(AgentState)
    
    # --- Add Nodes ---
    workflow.add_node("greeter", greeter_node)  # ADD THIS
    workflow.add_node("analyzer", analyzer_node)
    workflow.add_node("router", router_node)
    workflow.add_node("consultant", consultant_node)
    workflow.add_node("playbook_selector", playbook_selector_node)
    workflow.add_node("executor", executor_node)
    workflow.add_node("setup", initial_setup_node)
    
    # --- Define Flow ---
    
    # 1. Start with Greeter (Filter casual messages)
    workflow.add_edge(START, "greeter")  # CHANGED FROM "analyzer"
    
    # 2. Conditional: Analyze or Skip
    workflow.add_conditional_edges(
        "greeter",
        should_analyze,
        {
            "analyzer": "analyzer",
            "router": "router", 
            "end": END
        }
    )
    
    # 3. Move to Decision Making
    workflow.add_edge("analyzer", "router")
    
    # 4. Conditional Routing (The "Split")
    workflow.add_conditional_edges(
        "router",
        route_next_step,
        {
            "setup": "setup",
            "consultant": "consultant",
            "playbook_selector": "playbook_selector",
            "executor": "executor"
        }
    )
    
    # 5. Closing the Loops
    workflow.add_edge("playbook_selector", "executor")
    
    # End states
    workflow.add_edge("consultant", END)
    workflow.add_conditional_edges(
        "executor",
        should_continue_play,
        {
            "executor": "executor", 
            "end": END
        }
    )
    workflow.add_edge("setup", END)

    return workflow.compile()

# Export the compiled graph
graph = create_graph()