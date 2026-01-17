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
            stats=stats # Storing raw stats for the AI to reference
        )

# Global storage for all NBA teams
NBA_DATA: Dict[str, List[PlayerProfile]] = {}

def load_data_from_csv(file_path: str = "nba_stats_2025.csv"):
    """
    Parses the game-by-game stats CSV. 
    Aggregates data to create a tactical profile for each player.
    """
    global NBA_DATA
    if not os.path.exists(file_path):
        print(f"File {file_path} not found.")
        return

    # Temporary storage to handle multiple entries for the same player
    player_agg = {}

    with open(file_path, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row['Player']
            team = row['Tm']
            
            # Use only the most recent/relevant entry or average them
            # For simplicity, we'll take the first occurrence in the file (latest games usually)
            if name in player_agg:
                continue
                
            stats = {
                "pts": float(row['PTS']),
                "ast": float(row['AST']),
                "trb": float(row['TRB']),
                "blk": float(row['BLK']),
                "stl": float(row['STL']),
                "three_p_pct": float(row['3P%']) if row['3P%'] else 0,
                "mp": float(row['MP'])
            }

            # Determine tactical traits based on these numbers
            archetype, skills, ranges, pos = _analyze_player_traits(stats)
            
            p_id = f"{team.lower()}-{name.replace(' ', '-').lower()}"
            
            profile = PlayerProfile(
                id=p_id,
                name=name,
                team=team,
                position=pos,
                archetype=archetype,
                shooting_ranges=ranges,
                key_skills=skills,
                speed=_calculate_speed(pos, stats),
                stats=stats
            )
            
            if team not in NBA_DATA:
                NBA_DATA[team] = []
            NBA_DATA[team].append(profile)

def _analyze_player_traits(stats):
    """
    Heuristic engine: Categorizes players based on their box score.
    """
    skills = []
    ranges = ["Paint"]
    
    # 1. Determine Position & Archetype
    if stats['ast'] >= 5:
        pos, arch = "G", "Floor General"
        skills += ["Playmaking", "Ball Handling"]
        ranges += ["Top3", "Wing3"]
    elif stats['trb'] >= 9 or stats['blk'] >= 1.5:
        pos, arch = "C", "Interior Force"
        skills += ["Rebounding", "Rim Protection"]
    elif stats['three_p_pct'] > 0.40 and stats['pts'] > 15:
        pos, arch = "F/G", "Sharpshooter"
        skills += ["3PT Shooting", "Off-ball Movement"]
        ranges += ["Top3", "Wing3", "Corner3"]
    else:
        pos, arch = "F", "Two-Way Player"
        skills += ["Defense", "Versatility"]
        ranges += ["Mid"]

    # 2. Add specific skills
    if stats['three_p_pct'] > 0.33: ranges += ["Corner3"]
    if stats['stl'] >= 1.5: skills.append("Passing Lane Interceptor")
    
    return arch, skills, ranges, pos

def _calculate_speed(pos, stats):
    """Bigger players are slower, guards are faster."""
    base_speed = 7
    if pos == "G": base_speed = 8
    if pos == "C": base_speed = 5
    return base_speed

# --- Helper Functions for the AI ---

def get_team_roster(team_abbr: str) -> List[Dict]:
    """Get roster by team abbreviation (e.g., 'LAL', 'BOS')"""
    if not NBA_DATA:
        load_data_from_csv()
    return NBA_DATA.get(team_abbr, [])

def get_player_by_id(player_id: str, roster: List[Dict]) -> Optional[Dict]:
    for player in roster:
        if player["id"] == player_id:
            return player
    return None