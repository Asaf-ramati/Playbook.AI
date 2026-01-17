"""
NBA Teams Constants
כל 30 קבוצות ה-NBA עם שמות מלאים וקיצורים
"""

# רשימת כל קבוצות ה-NBA
NBA_TEAMS = {
    # Eastern Conference - Atlantic Division
    "BOSTON_CELTICS": {
        "full_name": "Boston Celtics",
        "abbreviation": "BOS",
        "city": "Boston",
        "name": "Celtics"
    },
    "BROOKLYN_NETS": {
        "full_name": "Brooklyn Nets",
        "abbreviation": "BKN",
        "city": "Brooklyn",
        "name": "Nets"
    },
    "NEW_YORK_KNICKS": {
        "full_name": "New York Knicks",
        "abbreviation": "NYK",
        "city": "New York",
        "name": "Knicks"
    },
    "PHILADELPHIA_76ERS": {
        "full_name": "Philadelphia 76ers",
        "abbreviation": "PHI",
        "city": "Philadelphia",
        "name": "76ers"
    },
    "TORONTO_RAPTORS": {
        "full_name": "Toronto Raptors",
        "abbreviation": "TOR",
        "city": "Toronto",
        "name": "Raptors"
    },
    
    # Eastern Conference - Central Division
    "CHICAGO_BULLS": {
        "full_name": "Chicago Bulls",
        "abbreviation": "CHI",
        "city": "Chicago",
        "name": "Bulls"
    },
    "CLEVELAND_CAVALIERS": {
        "full_name": "Cleveland Cavaliers",
        "abbreviation": "CLE",
        "city": "Cleveland",
        "name": "Cavaliers"
    },
    "DETROIT_PISTONS": {
        "full_name": "Detroit Pistons",
        "abbreviation": "DET",
        "city": "Detroit",
        "name": "Pistons"
    },
    "INDIANA_PACERS": {
        "full_name": "Indiana Pacers",
        "abbreviation": "IND",
        "city": "Indiana",
        "name": "Pacers"
    },
    "MILWAUKEE_BUCKS": {
        "full_name": "Milwaukee Bucks",
        "abbreviation": "MIL",
        "city": "Milwaukee",
        "name": "Bucks"
    },
    
    # Eastern Conference - Southeast Division
    "ATLANTA_HAWKS": {
        "full_name": "Atlanta Hawks",
        "abbreviation": "ATL",
        "city": "Atlanta",
        "name": "Hawks"
    },
    "CHARLOTTE_HORNETS": {
        "full_name": "Charlotte Hornets",
        "abbreviation": "CHA",
        "city": "Charlotte",
        "name": "Hornets"
    },
    "MIAMI_HEAT": {
        "full_name": "Miami Heat",
        "abbreviation": "MIA",
        "city": "Miami",
        "name": "Heat"
    },
    "ORLANDO_MAGIC": {
        "full_name": "Orlando Magic",
        "abbreviation": "ORL",
        "city": "Orlando",
        "name": "Magic"
    },
    "WASHINGTON_WIZARDS": {
        "full_name": "Washington Wizards",
        "abbreviation": "WAS",
        "city": "Washington",
        "name": "Wizards"
    },
    
    # Western Conference - Northwest Division
    "DENVER_NUGGETS": {
        "full_name": "Denver Nuggets",
        "abbreviation": "DEN",
        "city": "Denver",
        "name": "Nuggets"
    },
    "MINNESOTA_TIMBERWOLVES": {
        "full_name": "Minnesota Timberwolves",
        "abbreviation": "MIN",
        "city": "Minnesota",
        "name": "Timberwolves"
    },
    "OKLAHOMA_CITY_THUNDER": {
        "full_name": "Oklahoma City Thunder",
        "abbreviation": "OKC",
        "city": "Oklahoma City",
        "name": "Thunder"
    },
    "PORTLAND_TRAIL_BLAZERS": {
        "full_name": "Portland Trail Blazers",
        "abbreviation": "POR",
        "city": "Portland",
        "name": "Trail Blazers"
    },
    "UTAH_JAZZ": {
        "full_name": "Utah Jazz",
        "abbreviation": "UTA",
        "city": "Utah",
        "name": "Jazz"
    },
    
    # Western Conference - Pacific Division
    "GOLDEN_STATE_WARRIORS": {
        "full_name": "Golden State Warriors",
        "abbreviation": "GSW",
        "city": "Golden State",
        "name": "Warriors"
    },
    "LA_CLIPPERS": {
        "full_name": "LA Clippers",
        "abbreviation": "LAC",
        "city": "Los Angeles",
        "name": "Clippers"
    },
    "LA_LAKERS": {
        "full_name": "LA Lakers",
        "abbreviation": "LAL",
        "city": "Los Angeles",
        "name": "Lakers"
    },
    "PHOENIX_SUNS": {
        "full_name": "Phoenix Suns",
        "abbreviation": "PHX",
        "city": "Phoenix",
        "name": "Suns"
    },
    "SACRAMENTO_KINGS": {
        "full_name": "Sacramento Kings",
        "abbreviation": "SAC",
        "city": "Sacramento",
        "name": "Kings"
    },

    # Western Conference - Southwest Division
    "DALLAS_MAVERICKS": {
        "full_name": "Dallas Mavericks",
        "abbreviation": "DAL",
        "city": "Dallas",
        "name": "Mavericks"
    },
    "HOUSTON_ROCKETS": {
        "full_name": "Houston Rockets",
        "abbreviation": "HOU",
        "city": "Houston",
        "name": "Rockets"
    },
    "MEMPHIS_GRIZZLIES": {
        "full_name": "Memphis Grizzlies",
        "abbreviation": "MEM",
        "city": "Memphis",
        "name": "Grizzlies"
    },
    "NEW_ORLEANS_PELICANS": {
        "full_name": "New Orleans Pelicans",
        "abbreviation": "NOP",
        "city": "New Orleans",
        "name": "Pelicans"
    },
    "SAN_ANTONIO_SPURS": {
        "full_name": "San Antonio Spurs",
        "abbreviation": "SAS",
        "city": "San Antonio",
        "name": "Spurs"
    }
}


def normalize_team_name(team_input: str) -> str:
    """
    מנרמל את שם הקבוצה שהמשתמש הזין ומחזיר את השם המלא הרשמי.
    לא רגיש לאותיות גדולות/קטנות.

    Args:
        team_input: שם הקבוצה שהמשתמש הזין (יכול להיות שם מלא, עיר, שם קבוצה, או קיצור)

    Returns:
        השם המלא הרשמי של הקבוצה

    Raises:
        ValueError: אם הקבוצה לא נמצאה

    Examples:
        >>> normalize_team_name("lakers")
        "LA Lakers"
        >>> normalize_team_name("BOS")
        "Boston Celtics"
        >>> normalize_team_name("golden state warriors")
        "Golden State Warriors"
    """
    team_input_lower = team_input.strip().lower()

    # חיפוש בכל הקבוצות
    for team_key, team_data in NBA_TEAMS.items():
        # בדיקה מול שם מלא
        if team_data["full_name"].lower() == team_input_lower:
            return team_data["full_name"]

        # בדיקה מול קיצור
        if team_data["abbreviation"].lower() == team_input_lower:
            return team_data["full_name"]

        # בדיקה מול שם העיר
        if team_data["city"].lower() == team_input_lower:
            return team_data["full_name"]

        # בדיקה מול שם הקבוצה בלבד
        if team_data["name"].lower() == team_input_lower:
            return team_data["full_name"]

        # בדיקה אם השם מכיל את שם הקבוצה או העיר
        if team_data["name"].lower() in team_input_lower or team_input_lower in team_data["name"].lower():
            return team_data["full_name"]

    # אם לא נמצא - זרוק שגיאה עם רשימת קבוצות אפשריות
    available_teams = [team["full_name"] for team in NBA_TEAMS.values()]
    raise ValueError(
        f"קבוצה '{team_input}' לא נמצאה. "
        f"קבוצות זמינות: {', '.join(available_teams)}"
    )


def get_team_abbreviation(team_name: str) -> str:
    """
    מחזיר את הקיצור של הקבוצה

    Args:
        team_name: שם הקבוצה (יכול להיות בכל פורמט)

    Returns:
        קיצור הקבוצה (למשל "LAL", "BOS")
    """
    normalized_name = normalize_team_name(team_name)

    for team_data in NBA_TEAMS.values():
        if team_data["full_name"] == normalized_name:
            return team_data["abbreviation"]

    return ""


def get_all_team_names() -> list[str]:
    """
    מחזיר רשימה של כל שמות הקבוצות המלאים

    Returns:
        רשימת שמות קבוצות
    """
    return [team["full_name"] for team in NBA_TEAMS.values()]


def is_valid_team(team_input: str) -> bool:
    """
    בודק אם שם הקבוצה תקין

    Args:
        team_input: שם הקבוצה לבדיקה

    Returns:
        True אם הקבוצה תקינה, False אחרת
    """
    try:
        normalize_team_name(team_input)
        return True
    except ValueError:
        return False

