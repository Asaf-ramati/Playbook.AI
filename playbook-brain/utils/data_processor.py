import pandas as pd
from graph.roster import PlayerProfile

def load_nba_data_from_csv(file_path: str = "nba_stats_cleaned.csv"):
    # קריאת הקובץ הנקי
    df = pd.read_csv(file_path)
    
    nba_teams = {}
    
    for _, row in df.iterrows():
        # מניעת חלוקה באפס במידה ושחקן לא שיחק
        gp = row['GP'] if row['GP'] > 0 else 1
        
        # חישוב ממוצעים למשחק כי ה-DB הוא Totals
        # זה קריטי כדי שה-Analyzer יבין מה הכוח האמיתי של השחקן ברגע נתון
        stats = {
            "pts": round(row['PTS'] / gp, 1),
            "ast": round(row['AST'] / gp, 1),
            "trb": round(row['REB'] / gp, 1),
            "blk": round(row['BLK'] / gp, 1),
            "stl": round(row['STL'] / gp, 1),
            "three_p_pct": row['3P%'],
            "plus_minus_avg": round(row['PLUS_MINUS'] / gp, 1),
            "mp": round(row['Min'] / gp, 1)
        }

        # שימוש בלוגיקה לזיהוי עמדה ותכונות
        archetype, skills, ranges, pos = _analyze_player_traits(stats)
        
        team_abbr = row['Team'] # השם המדויק מה-CSV הנקי
        player_name = row['Player']
        player_id = f"{team_abbr.lower()}-{player_name.replace(' ', '-').lower()}"
        
        profile = PlayerProfile(
            id=player_id,
            name=player_name,
            team=team_abbr,
            position=pos,
            archetype=archetype,
            shooting_ranges=ranges,
            key_skills=skills,
            speed=8 if pos == "G" else 6, # גארדים מהירים יותר בסימולציה
            stats=stats
        )
        
        if team_abbr not in nba_teams:
            nba_teams[team_abbr] = []
        nba_teams[team_abbr].append(profile)
            
    return nba_teams

def _analyze_player_traits(stats):
    """מנוע החוקים שקובע מי השחקן לפי המספרים שלו"""
    skills = []
    ranges = ["Paint"]
    
    # זיהוי קלעי שלשות
    if stats['three_p_pct'] > 36:
        skills.append("3PT Specialist")
        ranges += ["Top3", "Wing3", "Corner3"]
    
    # קביעת עמדה וארכיטיפ
    if stats['ast'] > 5:
        return "Floor General", skills + ["Playmaking"], ranges + ["Top3"], "G"
    elif stats['trb'] > 8:
        return "Interior Anchor", skills + ["Rim Protection"], ranges, "C"
    else:
        return "Versatile Forward", skills + ["Defense"], ranges + ["Mid", "Corner3"], "F"