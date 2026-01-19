"""
NBA Teams Constants & Court Configuration
This file contains all system constants: teams, abbreviations, and court dimensions.
"""

# --- Court dimensions (needed for Frontend and movement calculations) ---
COURT_WIDTH = 660
COURT_HEIGHT = 550

# --- List of all NBA teams ---
NBA_TEAMS = {
    # Eastern Conference - Atlantic Division
    "BOSTON_CELTICS": {"full_name": "Boston Celtics", "abbreviation": "BOS", "city": "Boston", "name": "Celtics"},
    "BROOKLYN_NETS": {"full_name": "Brooklyn Nets", "abbreviation": "BKN", "city": "Brooklyn", "name": "Nets"},
    "NEW_YORK_KNICKS": {"full_name": "New York Knicks", "abbreviation": "NYK", "city": "New York", "name": "Knicks"},
    "PHILADELPHIA_76ERS": {"full_name": "Philadelphia 76ers", "abbreviation": "PHI", "city": "Philadelphia", "name": "76ers"},
    "TORONTO_RAPTORS": {"full_name": "Toronto Raptors", "abbreviation": "TOR", "city": "Toronto", "name": "Raptors"},
    
    # Eastern Conference - Central Division
    "CHICAGO_BULLS": {"full_name": "Chicago Bulls", "abbreviation": "CHI", "city": "Chicago", "name": "Bulls"},
    "CLEVELAND_CAVALIERS": {"full_name": "Cleveland Cavaliers", "abbreviation": "CLE", "city": "Cleveland", "name": "Cavaliers"},
    "DETROIT_PISTONS": {"full_name": "Detroit Pistons", "abbreviation": "DET", "city": "Detroit", "name": "Pistons"},
    "INDIANA_PACERS": {"full_name": "Indiana Pacers", "abbreviation": "IND", "city": "Indiana", "name": "Pacers"},
    "MILWAUKEE_BUCKS": {"full_name": "Milwaukee Bucks", "abbreviation": "MIL", "city": "Milwaukee", "name": "Bucks"},
    
    # Eastern Conference - Southeast Division
    "ATLANTA_HAWKS": {"full_name": "Atlanta Hawks", "abbreviation": "ATL", "city": "Atlanta", "name": "Hawks"},
    "CHARLOTTE_HORNETS": {"full_name": "Charlotte Hornets", "abbreviation": "CHA", "city": "Charlotte", "name": "Hornets"},
    "MIAMI_HEAT": {"full_name": "Miami Heat", "abbreviation": "MIA", "city": "Miami", "name": "Heat"},
    "ORLANDO_MAGIC": {"full_name": "Orlando Magic", "abbreviation": "ORL", "city": "Orlando", "name": "Magic"},
    "WASHINGTON_WIZARDS": {"full_name": "Washington Wizards", "abbreviation": "WAS", "city": "Washington", "name": "Wizards"},
    
    # Western Conference - Northwest Division
    "DENVER_NUGGETS": {"full_name": "Denver Nuggets", "abbreviation": "DEN", "city": "Denver", "name": "Nuggets"},
    "MINNESOTA_TIMBERWOLVES": {"full_name": "Minnesota Timberwolves", "abbreviation": "MIN", "city": "Minnesota", "name": "Timberwolves"},
    "OKLAHOMA_CITY_THUNDER": {"full_name": "Oklahoma City Thunder", "abbreviation": "OKC", "city": "Oklahoma City", "name": "Thunder"},
    "PORTLAND_TRAIL_BLAZERS": {"full_name": "Portland Trail Blazers", "abbreviation": "POR", "city": "Portland", "name": "Trail Blazers"},
    "UTAH_JAZZ": {"full_name": "Utah Jazz", "abbreviation": "UTA", "city": "Utah", "name": "Jazz"},
    
    # Western Conference - Pacific Division
    "GOLDEN_STATE_WARRIORS": {"full_name": "Golden State Warriors", "abbreviation": "GSW", "city": "Golden State", "name": "Warriors"},
    "LA_CLIPPERS": {"full_name": "LA Clippers", "abbreviation": "LAC", "city": "Los Angeles", "name": "Clippers"},
    "LA_LAKERS": {"full_name": "LA Lakers", "abbreviation": "LAL", "city": "Los Angeles", "name": "Lakers"},
    "PHOENIX_SUNS": {"full_name": "Phoenix Suns", "abbreviation": "PHX", "city": "Phoenix", "name": "Suns"},
    "SACRAMENTO_KINGS": {"full_name": "Sacramento Kings", "abbreviation": "SAC", "city": "Sacramento", "name": "Kings"},

    # Western Conference - Southwest Division
    "DALLAS_MAVERICKS": {"full_name": "Dallas Mavericks", "abbreviation": "DAL", "city": "Dallas", "name": "Mavericks"},
    "HOUSTON_ROCKETS": {"full_name": "Houston Rockets", "abbreviation": "HOU", "city": "Houston", "name": "Rockets"},
    "MEMPHIS_GRIZZLIES": {"full_name": "Memphis Grizzlies", "abbreviation": "MEM", "city": "Memphis", "name": "Grizzlies"},
    "NEW_ORLEANS_PELICANS": {"full_name": "New Orleans Pelicans", "abbreviation": "NOP", "city": "New Orleans", "name": "Pelicans"},
    "SAN_ANTONIO_SPURS": {"full_name": "San Antonio Spurs", "abbreviation": "SAS", "city": "San Antonio", "name": "Spurs"}
}

def get_team_color(abbr: str) -> str:
    """
    Returns the official Hex Color for an NBA team.
    """
    colors = {
        "ATL": "#C8102E", "BOS": "#007A33", "BKN": "#000000", "CHA": "#1D1160",
        "CHI": "#CE1141", "CLE": "#860038", "DAL": "#00538C", "DEN": "#0E2240",
        "DET": "#C8102E", "GSW": "#1D428A", "HOU": "#CE1141", "IND": "#002D62",
        "LAC": "#C8102E", "LAL": "#552583", "MEM": "#5D76A9", "MIA": "#98002E",
        "MIL": "#00471B", "MIN": "#0C2340", "NOP": "#0C2340", "NYK": "#006BB6",
        "OKC": "#007AC1", "ORL": "#0077C0", "PHI": "#006BB6", "PHX": "#1D1160",
        "POR": "#E03A3E", "SAC": "#5A2D81", "SAS": "#C4CED4", "TOR": "#CE1141",
        "UTA": "#002B5C", "WAS": "#002B5C"
    }
    return colors.get(abbr.upper(), "#000000")


def normalize_team_name(team_input: str) -> str:
    """
    Normalizes the team name entered by the user and returns the official full name.
    """
    if not team_input:
        raise ValueError("Team name is empty")

    team_input_lower = team_input.strip().lower()

    for team_data in NBA_TEAMS.values():
        # Check against all possible variations
        if (team_data["full_name"].lower() == team_input_lower or
            team_data["abbreviation"].lower() == team_input_lower or
            team_data["city"].lower() == team_input_lower or
            team_data["name"].lower() == team_input_lower):
            return team_data["full_name"]

        # Smart check for inclusion (e.g., "Coach of the Lakers" -> will find "Lakers")
        if team_data["name"].lower() in team_input_lower:
            return team_data["full_name"]

    # Throw error if not found - the Router will catch this
    raise ValueError(f"Team '{team_input}' not found.")

def get_team_abbreviation(team_name: str) -> str:
    """
    Receives a free-form name (e.g., 'Lakers') and returns the abbreviation from CSV (e.g., 'LAL')
    """
    try:
        normalized_name = normalize_team_name(team_name)
        for team_data in NBA_TEAMS.values():
            if team_data["full_name"] == normalized_name:
                return team_data["abbreviation"]
    except ValueError:
        # If not found, return the original string abbreviated (as last resort)
        return team_name[:3].upper()

    return ""
