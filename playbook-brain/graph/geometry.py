import math
from typing import List, Dict, Any

# Court settings (adapted for your React Flow)
HOOP_POSITION = {"x": 400, "y": 50}
PAINT_AREA = {"x_min": 350, "x_max": 450, "y_max": 200}
THREE_POINT_RADIUS = 300 # Approximately, in screen units

def get_distance(p1: Dict[str, float], p2: Dict[str, float]) -> float:
    """Calculate Euclidean distance between two points"""
    return math.sqrt((p1["x"] - p2["x"])**2 + (p1["y"] - p2["y"])**2)

def identify_zone(position: Dict[str, float]) -> str:
    """Returns the name of the court zone where the player is located"""
    x, y = position["x"], position["y"]

    # Check paint area
    if PAINT_AREA["x_min"] <= x <= PAINT_AREA["x_max"] and y <= PAINT_AREA["y_max"]:
        return "PAINT"

    # Check distance from hoop (to determine three-point line)
    dist_to_hoop = get_distance(position, HOOP_POSITION)

    if dist_to_hoop > THREE_POINT_RADIUS:
        if y < 100: return "CORNER_3"
        if x < 250 or x > 550: return "WING_3"
        return "TOP_3"

    # Mid-range area
    return "MID_RANGE"

def analyze_spacing(players: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Analyzes the spacing between offensive players.
    Returns a score (0-10) and a list of player pairs that are too close to each other.
    """
    if len(players) < 2:
        return {"score": 10, "clogged_pairs": []}

    clogged_pairs = []
    min_spacing_threshold = 70.0 # Desired minimum distance between players
    total_penalty = 0

    for i in range(len(players)):
        for j in range(i + 1, len(players)):
            p1 = players[i]
            p2 = players[j]

            # Ignore the ball in player spacing calculations
            if p1['id'] == 'ball' or p2['id'] == 'ball':
                continue

            dist = get_distance(p1["position"], p2["position"])

            if dist < min_spacing_threshold:
                pair_names = f"{p1.get('data', {}).get('name')} & {p2.get('data', {}).get('name')}"
                clogged_pairs.append(pair_names)
                total_penalty += (min_spacing_threshold - dist)

    # Calculate score: start from 10 and deduct points for congestion
    score = max(0, 10 - (total_penalty / 20))

    return {
        "score": round(score, 1),
        "clogged_pairs": clogged_pairs,
        "is_clogged": score < 6
    }