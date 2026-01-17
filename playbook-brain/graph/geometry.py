import math
from typing import List, Dict, Any

# הגדרות המגרש (מותאם ל-React Flow שלך)
HOOP_POSITION = {"x": 400, "y": 50} 
PAINT_AREA = {"x_min": 350, "x_max": 450, "y_max": 200}
THREE_POINT_RADIUS = 300 # בערך, ביחידות של המסך

def get_distance(p1: Dict[str, float], p2: Dict[str, float]) -> float:
    """חישוב מרחק אוקלידי בין שתי נקודות"""
    return math.sqrt((p1["x"] - p2["x"])**2 + (p1["y"] - p2["y"])**2)

def identify_zone(position: Dict[str, float]) -> str:
    """מחזיר את שם האזור במגרש בו השחקן נמצא"""
    x, y = position["x"], position["y"]
    
    # בדיקת אזור הצבע (Paint)
    if PAINT_AREA["x_min"] <= x <= PAINT_AREA["x_max"] and y <= PAINT_AREA["y_max"]:
        return "PAINT"
    
    # בדיקת מרחק מהסל (לקביעת קשת השלוש)
    dist_to_hoop = get_distance(position, HOOP_POSITION)
    
    if dist_to_hoop > THREE_POINT_RADIUS:
        if y < 100: return "CORNER_3"
        if x < 250 or x > 550: return "WING_3"
        return "TOP_3"
    
    # אזור הביניים (Mid-Range)
    return "MID_RANGE"

def analyze_spacing(players: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    מנתח את הריווח בין שחקני ההתקפה.
    מחזיר ציון (0-10) ורשימה של זוגות שחקנים שקרובים מדי זה לזה.
    """
    if len(players) < 2:
        return {"score": 10, "clogged_pairs": []}

    clogged_pairs = []
    min_spacing_threshold = 70.0 # מרחק מינימלי רצוי בין שחקנים
    total_penalty = 0

    for i in range(len(players)):
        for j in range(i + 1, len(players)):
            p1 = players[i]
            p2 = players[j]
            
            # מתעלמים מהכדור בחישוב ריווח שחקנים
            if p1['id'] == 'ball' or p2['id'] == 'ball':
                continue

            dist = get_distance(p1["position"], p2["position"])
            
            if dist < min_spacing_threshold:
                pair_names = f"{p1.get('data', {}).get('name')} & {p2.get('data', {}).get('name')}"
                clogged_pairs.append(pair_names)
                total_penalty += (min_spacing_threshold - dist)

    # חישוב ציון: מתחילים מ-10 ומורידים נקודות על צפיפות
    score = max(0, 10 - (total_penalty / 20)) 
    
    return {
        "score": round(score, 1),
        "clogged_pairs": clogged_pairs,
        "is_clogged": score < 6
    }