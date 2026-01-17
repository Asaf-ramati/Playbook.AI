import csv
import os
from typing import Dict, List, Optional

class PlayerProfile(dict):
    def __init__(self, id, name, team, position, archetype, shooting_ranges, key_skills, speed, stats):
        super().__init__(
            id=id,
            name=name,
            team=team,
            position=position,
            archetype=archetype,
            shooting_ranges=shooting_ranges,
            key_skills=key_skills,
            speed=speed,
            stats=stats 
        )

# Global storage for all NBA teams
NBA_DATA: Dict[str, List[PlayerProfile]] = {}

def get_team_roster(team_abbr: str) -> List[Dict]:
    """
    מחזיר את סגל השחקנים לפי קיצור הקבוצה (למשל 'LAL', 'OKC').
    אם הנתונים טרם נטענו, הוא קורא למעבד הנתונים.
    """
    global NBA_DATA
    if not NBA_DATA:
        # טעינה דינמית כדי למנוע Circular Import
        from utils.data_processor import load_nba_data_from_csv
        # וודא שהשם כאן תואם לקובץ הנקי שלך
        NBA_DATA = load_nba_data_from_csv("nba_stats_cleaned.csv")
    
    return NBA_DATA.get(team_abbr, [])

def get_player_by_id(player_id: str, roster: List[Dict]) -> Optional[Dict]:
    """שליפת שחקן ספציפי מתוך סגל"""
    for player in roster:
        if player["id"] == player_id:
            return player
    return None

def load_player_capabilities(player_id: str, team_id: str) -> str:
    """הצגת יכולות השחקן כטקסט עבור ה-LLM"""
    roster = get_team_roster(team_id)
    profile = get_player_by_id(player_id, roster)
    
    if not profile:
        return "Unknown player."
        
    skills = ", ".join(profile['key_skills'])
    stats = profile['stats']
    return (f"{profile['name']} ({profile['position']}): {profile['archetype']}. "
            f"Skills: {skills}. Avg Points: {stats['pts']}, Assists: {stats['ast']}.")