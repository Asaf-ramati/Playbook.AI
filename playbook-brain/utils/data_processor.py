import pandas as pd
from graph.roster import PlayerProfile

def load_nba_data_from_csv(file_path: str):
    # 1. Read the CSV
    df = pd.read_csv(file_path)
    
    # 2. Aggregation: The CSV has one row per game. 
    # We want one row per player with their latest team and average stats.
    # We take the last occurrence to get the most recent team (Tm)
    df_unique = df.drop_duplicates(subset=['Player'], keep='last').copy()
    
    nba_teams = {}
    
    for _, row in df_unique.iterrows():
        # Match the CSV headers: 'Tm' instead of 'Team'
        team_abbr = row['Tm'] 
        player_name = row['Player']
        player_id = f"{team_abbr.lower()}-{player_name.replace(' ', '-').lower()}"
        
        # Heuristic for Position (since 'Position' isn't in this CSV)
        # We can guess by their stats: high TRB/BLK = Center, high AST = Guard
        ast = row.get('AST', 0)
        trb = row.get('TRB', 0)
        
        if ast > 4:
            pos, arch = "G", "Playmaker"
            skills, ranges = ["Passing", "Handles"], ["Top3", "Wing3", "Paint"]
        elif trb > 8:
            pos, arch = "C", "Big Man"
            skills, ranges = ["Rebounding", "Post"], ["Paint"]
        else:
            pos, arch = "F", "Wing"
            skills, ranges = ["Defense", "Shooting"], ["Mid", "Corner3", "Paint"]

        # Create the profile using the Stats in the CSV
        profile = PlayerProfile(
            id=player_id,
            name=player_name,
            position=pos,
            archetype=arch,
            shooting_ranges=ranges,
            key_skills=skills,
            speed=7 # Baseline
        )
        
        if team_abbr not in nba_teams:
            nba_teams[team_abbr] = []
        nba_teams[team_abbr].append(profile)
            
    return nba_teams