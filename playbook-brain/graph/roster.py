from typing import Dict, List, Optional

class PlayerProfile(dict):
    def __init__(self, id, name, position, archetype, shooting_ranges, key_skills, speed):
        super().__init__(
            id=id,
            name=name,
            position=position,
            archetype=archetype,
            shooting_ranges=shooting_ranges,
            key_skills=key_skills,
            speed=speed
        )
        
MOCK_DB = {
    "lakers_mock": [
        PlayerProfile(
            id="team1-pg",
            name="D'Angelo Russell",
            position="PG",
            archetype="Shot Creator",
            shooting_ranges=["Top3", "Wing3", "Mid"],
            key_skills=["Passing", "Pick & Roll", "3PT"],
            speed=7
        ),
        PlayerProfile(
            id="team1-sg",
            name="Austin Reaves",
            position="SG",
            archetype="Secondary Playmaker",
            shooting_ranges=["Wing3", "Mid", "Paint"],
            key_skills=["Drives", "Foul Drawing", "IQ"],
            speed=7
        ),
        PlayerProfile(
            id="team1-sf",
            name="LeBron James",
            position="SF",
            archetype="Point Forward",
            shooting_ranges=["Paint", "Top3", "Mid"],
            key_skills=["Elite Passing", "Power Driving", "Floor General"],
            speed=8
        ),
        PlayerProfile(
            id="team1-pf",
            name="Rui Hachimura",
            position="PF",
            archetype="Stretch 4",
            shooting_ranges=["Mid", "Corner3", "Paint"],
            key_skills=["Mid-range", "Transition Running", "Post-up"],
            speed=7
        ),
        PlayerProfile(
            id="team1-c",
            name="Anthony Davis",
            position="C",
            archetype="Two-Way Elite Big",
            shooting_ranges=["Paint", "Mid"],
            key_skills=["Elite Defense", "Rebounding", "Lob Threat"],
            speed=7
        )
    ],
    "warriors_mock": [
        PlayerProfile(
            id="team2-pg",
            name="Steph Curry",
            position="PG",
            archetype="Movement Shooter",
            shooting_ranges=["Top3", "Wing3", "Corner3", "Paint"],
            key_skills=["Elite 3PT", "Off-ball Movement", "Gravity"],
            speed=9
        ),
        PlayerProfile(
            id="team2-sg",
            name="Buddy Hield",
            position="SG",
            archetype="Sharpshooter",
            shooting_ranges=["Wing3", "Corner3"],
            key_skills=["3PT", "Catch & Shoot", "Spacing"],
            speed=7
        ),
        PlayerProfile(
            id="team2-sf",
            name="Andrew Wiggins",
            position="SF",
            archetype="3&D Wing",
            shooting_ranges=["Corner3", "Mid", "Paint"],
            key_skills=["On-ball Defense", "Slashing", "Athleticism"],
            speed=8
        ),
        PlayerProfile(
            id="team2-pf",
            name="Jonathan Kuminga",
            position="PF",
            archetype="Athletic Slasher",
            shooting_ranges=["Paint", "Mid"],
            key_skills=["Dunking", "Aggressive Driving", "Speed"],
            speed=9
        ),
        PlayerProfile(
            id="team2-c",
            name="Draymond Green",
            position="C",
            archetype="Defensive Anchor / Playmaker",
            shooting_ranges=["Paint"],
            key_skills=["Switch Defense", "Playmaking", "Screen Setting"],
            speed=6
        )
    ]
}

def load_player_capabilities(player_id: str, team_id: str) -> str:
    """
    פונקציה שמחזירה תיאור טקסטואלי של יכולות השחקן עבור ה-LLM.
    זה מאפשר למאמן להבין *מי* נמצא בעמדה מסוימת.
    """
    roster = get_team_roster(team_id)
    profile = get_player_by_id(player_id, roster)
    
    if not profile:
        return "Unknown player capabilities."
        
    skills_str = ", ".join(profile['skills'])
    return f"{profile['name']} is a {profile['position']} specialized in {skills_str}. Shooting range: {profile['shooting_range']}."


def get_team_roster(team_id: str = "lakers_mock") -> List[Dict]:
    """
    פונקציה זו מדמה קריאה ל-DB או API חיצוני.
    בעתיד תחליף את המימוש כאן לקריאה אמיתית.
    """
    return MOCK_DB.get(team_id, [])

def get_player_by_id(player_id: str, roster: List[Dict]) -> Optional[Dict]:
    """שליפת פרופיל שחקן לפי ID מתוך הסגל הנתון"""
    for player in roster:
        if player["id"] == player_id:
            return player
    return None