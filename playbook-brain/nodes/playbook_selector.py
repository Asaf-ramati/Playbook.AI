from typing import Dict, Any
from langchain_core.messages import AIMessage
from graph.state import AgentState
from coach.playbook import PLAYBOOK


def playbook_selector_node(state: AgentState) -> Dict[str, Any]:
    """
    The Librarian.
    Retrieves the specific play details from the static PLAYBOOK database.
    It prepares the data for the Executor but does NOT move players yet.
    """
    play_id = state.get("target_play")
    
    # Attempt to retrieve the play
    selected_play = PLAYBOOK.get(play_id)
    
    # Fallback logic if the Router selected a non-existent play
    if not selected_play:
        # Default to basic spacing if the specific play isn't found
        selected_play = PLAYBOOK.get("BASIC_SPACING") 
        msg = f"Could not find exact play '{play_id}', defaulting to Basic Spacing."
    else:
        msg = f"Preparing to execute: {selected_play['name']}..."

    # We return 'selected_play' so the Executor can access it
    return {
        "selected_play": selected_play,
        "messages": [AIMessage(content=msg)]
    }
