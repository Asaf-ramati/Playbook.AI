import json
from langchain_core.messages import AIMessage
from graph.state import AgentState
from .llm_utils import get_llm
from .constants import COURT_ZONES
from graph.constants import COURT_WIDTH, COURT_HEIGHT


def clamp_to_court(coords):
    """Ensure coordinates stay within court boundaries"""
    return {
        "x": max(0, min(coords["x"], COURT_WIDTH)),
        "y": max(0, min(coords["y"], COURT_HEIGHT))
    }


def generative_play_node(state: AgentState):
    llm = get_llm()
    user_message = state["messages"][-1].content
    current_players = state.get("players", [])

    # 1. Prepare Context for LLM
    # Create a simplified list of players for the prompt
    player_list_str = "\n".join([
        f"- Name: {p['data']['name']}, ID: {p['id']}, Current Role: {p['data']['position']}"
        for p in current_players if p['data']['side'] == "ATTACK"
    ])

    # Get available zones from constants
    available_zones = ", ".join(COURT_ZONES.keys())

    # 2. Define the Prompt
    prompt = f"""
    You are a Basketball Tactics Engine.
    Translate the user's specific movement request into a structured JSON format.

    **AVAILABLE PLAYERS (ATTACK):**
    {player_list_str}

    **AVAILABLE COURT ZONES:**
    {available_zones}

    **USER REQUEST:**
    "{user_message}"

    **INSTRUCTIONS:**
    1. Identify which players need to move based on the request.
    2. Assign a target ZONE from the list above to each moving player.
    3. If a player is not mentioned, do not move them.
    4. Return ONLY valid JSON.

    **JSON OUTPUT FORMAT:**
    {{
        "movements": [
            {{ "player_id": "PLAYER_ID_HERE", "target_zone": "ZONE_KEY_HERE" }},
            {{ "player_id": "ANOTHER_ID", "target_zone": "ANOTHER_ZONE" }}
        ]
    }}
    """

    # 3. Get LLM Response
    response = llm.invoke(prompt).content
    
    # Clean the response to ensure valid JSON (remove markdown code blocks if any)
    cleaned_response = response.replace("```json", "").replace("```", "").strip()
    
    try:
        data = json.loads(cleaned_response)
        movements = data.get("movements", [])
    except json.JSONDecodeError:
        return {
            "messages": [AIMessage(content="I couldn't process that specific movement. Try using standard play names.")]
        }

    # 4. Translate ZONES to COORDINATES (The Compiler)
    # This prepares the data exactly how the Executor expects it
    updates_map = {}
    
    for move in movements:
        p_id = move["player_id"]
        zone_key = move["target_zone"]
        
        if zone_key in COURT_ZONES:
            coords = COURT_ZONES[zone_key]
            updates_map[p_id] = clamp_to_court(coords) 

    # 5. Create executor-compatible step format
    generated_step = []

    for player_id, coords in updates_map.items():
        generated_step.append({
            "id": player_id,
            "x": coords["x"],
            "y": coords["y"]
        })

    # Add ball position (stays with first moving player)
    if updates_map:
        first_player_id = list(updates_map.keys())[0]
        ball_coords = updates_map[first_player_id]
        generated_step.append({
            "id": "ball",
            "x": ball_coords["x"],
            "y": ball_coords["y"]
        })

    return {
        "selected_play": {
            "id": "GEN_CUSTOM",
            "name": "Custom Tactical Move",
            "steps": [generated_step]
        },
        "current_step_index": 0,
        "intent": "PLAYBOOK",
        "messages": [AIMessage(content=f"Executing: {user_message}")]
    }