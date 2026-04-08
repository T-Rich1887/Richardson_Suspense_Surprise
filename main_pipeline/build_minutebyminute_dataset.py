# ============================================================================
# BUILD MINUTE-BY-MINUTE DATASET
# ============================================================================
# This script builds the minute-by-minute input file for the live odds and
# suspense calculations. It combines four data sources:
#   1. Predicted scoring rates from fit_scoring_rates.py
#   2. Empirical goal distribution from build_empirical_distribution.py
#   3. Goals and red card minutes from combine_season_files.py
#   4. Pre-match odds (already included in the predicted goals file)
#
# The output is one row per minute per match (92 rows per match), with
# cumulative score and red card counts built up minute by minute.
#
# INPUT:  - Combined goals/reds file
#         - Predicted goals CSV (output of fit_scoring_rates.py)
#         - Empirical goal distribution Excel file
# OUTPUT: Minute-by-minute CSV ready for calculate_live_odds.py
#
# NOTE ON TEAM NAME MAPPING:
# The predicted goals file uses team name abbreviations from the bookmaker
# odds source, while the goals/reds file uses full team names from the
# match event source. The TEAM_NAME_MAPPING below corrects this mismatch
# for each league. Users replicating with a different data source should
# verify their own team names match and adjust the mapping accordingly.
# Uncomment the mapping for your league and comment out the others.
# ============================================================================
 
import pandas as pd
import numpy as np
from pathlib import Path
 
# ============================================================================
# SETTINGS - EDIT THESE FOR YOUR LEAGUE
# ============================================================================
 
GOALS_REDS_FILE      = r"path/to/your/allseasons_goals_reds.xlsx"
PREDICTED_GOALS_FILE = r"path/to/your/predicted_goals.csv"
GOAL_DIST_FILE       = r"path/to/your/empirical_goal_distribution.xlsx"
OUTPUT_FILE          = r"path/to/your/get_minute_betting_odds.csv"
 
# ============================================================================
# TEAM NAME MAPPING
# Uncomment the mapping for your league. Users with different data sources
# should verify team names match between files and adjust as needed.
# ============================================================================
 
# --- EPL (England) ---
TEAM_NAME_MAPPING = {
    "Arsenal": "Arsenal",
    "Aston Villa": "Aston Villa",
    "Blackpool": "Blackpool",
    "Bournemouth": "Bournemouth",
    "Brentford": "Brentford",
    "Burnley": "Burnley",
    "Chelsea": "Chelsea",
    "Crystal Palace": "Crystal Palace",
    "Everton": "Everton",
    "Fulham": "Fulham",
    "Liverpool": "Liverpool",
    "Middlesbrough": "Middlesbrough",
    "Reading": "Reading",
    "Southampton": "Southampton",
    "Sunderland": "Sunderland",
    "Watford": "Watford",
    "Manchester Utd": "Manchester United",
    "Newcastle": "Newcastle United",
    "Norwich": "Norwich City",
    "Tottenham": "Tottenham Hotspur",
    "Stoke": "Stoke City",
    "Swansea": "Swansea City",
    "Wigan": "Wigan Athletic",
    "Bolton": "Bolton Wanderers",
    "Blackburn": "Blackburn Rovers",
    "Birmingham": "Birmingham City",
    "Cardiff": "Cardiff City",
    "Leeds": "Leeds United",
    "Leicester": "Leicester City",
    "Luton": "Luton Town",
    "Nottingham": "Nottingham Forest",
    "QPR": "Queens Park Rangers",
    "Sheffield Utd": "Sheffield United",
    "West Brom": "West Bromwich Albion",
    "West Ham": "West Ham United",
    "Wolves": "Wolverhampton Wanderers",
    "Manchester City": "Manchester City",
    "Huddersfield": "Huddersfield Town",
    "Hull": "Hull City",
    "Brighton": "Brighton & Hove Albion",
}
 
# --- Ligue 1 (France) ---
# TEAM_NAME_MAPPING = {
#     "Amiens": "Amiens",
#     "Angers": "Angers",
#     "Arles-Avignon": "Arles-Avignon",
#     "Auxerre": "Auxerre",
#     "Bastia": "Bastia",
#     "Bordeaux": "Bordeaux",
#     "Brest": "Brest",
#     "Caen": "Caen",
#     "Dijon": "Dijon",
#     "Guingamp": "Guingamp",
#     "Le Havre": "Le Havre",
#     "Lens": "Lens",
#     "Lille": "Lille",
#     "Lorient": "Lorient",
#     "Lyon": "Lyon",
#     "Marseille": "Marseille",
#     "Metz": "Metz",
#     "Monaco": "Monaco",
#     "Montpellier": "Montpellier",
#     "Nancy": "Nancy",
#     "Nantes": "Nantes",
#     "Nice": "Nice",
#     "Reims": "Reims",
#     "Rennes": "Rennes",
#     "Sochaux": "Sochaux",
#     "Strasbourg": "Strasbourg",
#     "Toulouse": "Toulouse",
#     "Troyes": "Troyes",
#     "Valenciennes": "Valenciennes",
#     "AC Ajaccio": "Ajaccio",
#     "GFC Ajaccio": "Gazélec Ajaccio",
#     "Clermont": "Clermont Foot",
#     "Nimes": "Nîmes",
#     "St Etienne": "Saint-Étienne",
#     "Thonon-Evian": "Évian",
#     "PSG": "Paris Saint-Germain",
#     "Paris SG": "Paris Saint-Germain",
# }
 
# --- Bundesliga (Germany) ---
# TEAM_NAME_MAPPING = {
#     "Augsburg": "Augsburg",
#     "Bayer Leverkusen": "Bayer Leverkusen",
#     "Bayern Munich": "Bayern Munich",
#     "Bochum": "Bochum",
#     "Dortmund": "Dortmund",
#     "Eintracht Frankfurt": "Eintracht Frankfurt",
#     "Freiburg": "Freiburg",
#     "Hamburger SV": "Hamburger SV",
#     "Heidenheim": "Heidenheim",
#     "Hoffenheim": "Hoffenheim",
#     "Kaiserslautern": "Kaiserslautern",
#     "RB Leipzig": "RB Leipzig",
#     "St. Pauli": "St. Pauli",
#     "Stuttgart": "Stuttgart",
#     "Union Berlin": "Union Berlin",
#     "Werder Bremen": "Werder Bremen",
#     "Wolfsburg": "Wolfsburg",
#     "Arminia Bielefeld": "Arminia",
#     "Braunschweig": "Eintracht Braunschweig",
#     "Darmstadt": "Darmstadt 98",
#     "Dusseldorf": "Düsseldorf",
#     "FC Koln": "Köln",
#     "Greuther Furth": "Greuther Fürth",
#     "Hannover": "Hannover 96",
#     "Hertha Berlin": "Hertha BSC",
#     "Ingolstadt": "Ingolstadt 04",
#     "Mainz": "Mainz 05",
#     "Nurnberg": "Nürnberg",
#     "Paderborn": "Paderborn 07",
#     "Schalke": "Schalke 04",
#     "B. Monchengladbach": "Mönchengladbach",
# }
 
# --- Serie A (Italy) ---
# TEAM_NAME_MAPPING = {
#     "Atalanta": "Atalanta",
#     "Bari": "Bari",
#     "Benevento": "Benevento",
#     "Bologna": "Bologna",
#     "Brescia": "Brescia",
#     "Cagliari": "Cagliari",
#     "Catania": "Catania",
#     "Cesena": "Cesena",
#     "Chievo": "Chievo",
#     "Cremonese": "Cremonese",
#     "Crotone": "Crotone",
#     "Empoli": "Empoli",
#     "Fiorentina": "Fiorentina",
#     "Frosinone": "Frosinone",
#     "Genoa": "Genoa",
#     "Juventus": "Juventus",
#     "Lazio": "Lazio",
#     "Lecce": "Lecce",
#     "Livorno": "Livorno",
#     "Monza": "Monza",
#     "Napoli": "Napoli",
#     "Novara": "Novara",
#     "Palermo": "Palermo",
#     "Parma": "Parma",
#     "Pescara": "Pescara",
#     "Salernitana": "Salernitana",
#     "Sampdoria": "Sampdoria",
#     "Sassuolo": "Sassuolo",
#     "Siena": "Siena",
#     "Spezia": "Spezia",
#     "Torino": "Torino",
#     "Udinese": "Udinese",
#     "Venezia": "Venezia",
#     "AC Carpi": "Carpi",
#     "AC Milan": "Milan",
#     "AS Roma": "Roma",
#     "Inter": "Internazionale",
#     "Spal": "SPAL",
#     "Verona": "Hellas Verona",
# }
 
# --- La Liga (Spain) ---
# TEAM_NAME_MAPPING = {
#     "Barcelona": "Barcelona",
#     "Celta Vigo": "Celta Vigo",
#     "Eibar": "Eibar",
#     "Elche": "Elche",
#     "Espanyol": "Espanyol",
#     "Getafe": "Getafe",
#     "Girona": "Girona",
#     "Huesca": "Huesca",
#     "Las Palmas": "Las Palmas",
#     "Levante": "Levante",
#     "Mallorca": "Mallorca",
#     "Osasuna": "Osasuna",
#     "Racing Santander": "Racing Santander",
#     "Rayo Vallecano": "Rayo Vallecano",
#     "Real Madrid": "Real Madrid",
#     "Real Sociedad": "Real Sociedad",
#     "Sevilla": "Sevilla",
#     "Valencia": "Valencia",
#     "Valladolid": "Valladolid",
#     "Villarreal": "Villarreal",
#     "Zaragoza": "Zaragoza",
#     "Alaves": "Alavés",
#     "Almeria": "Almería",
#     "Ath Bilbao": "Athletic Club",
#     "Atl. Madrid": "Atlético Madrid",
#     "Betis": "Real Betis",
#     "Cadiz CF": "Cádiz",
#     "Cordoba": "Córdoba",
#     "Dep. La Coruna": "Deportivo La Coruña",
#     "Gijon": "Sporting Gijón",
#     "Granada CF": "Granada",
#     "Hercules": "Hércules",
#     "Leganes": "Leganés",
#     "Malaga": "Málaga",
# }
 
# ============================================================================
# MAIN FUNCTION
# ============================================================================
 
def process_league_data():
 
    # ============================================================================
    # STEP 1: LOAD GOALS / REDS
    # ============================================================================
 
    df_goals_reds = pd.read_excel(GOALS_REDS_FILE)
 
    # ============================================================================
    # STEP 2: LOAD AND PROCESS PREDICTED GOALS DATA
    # ============================================================================
 
    league_data = pd.read_csv(PREDICTED_GOALS_FILE)
    league_data.columns = [c.lower() for c in league_data.columns]
 
    league_data['home_team'] = league_data['home_team'].map(TEAM_NAME_MAPPING).fillna(league_data['home_team'])
    league_data['away_team'] = league_data['away_team'].map(TEAM_NAME_MAPPING).fillna(league_data['away_team'])
 
    league_data['home_team'] = league_data['home_team'].str.strip()
    league_data['away_team'] = league_data['away_team'].str.strip()
 
    # Derive first season year from season code (e.g. 1011 -> 2010)
    league_data['year'] = league_data['season'].astype(str).str[:2].astype(int) + 2000
 
    league_data.insert(
        1,
        'match_id',
        league_data['year'].astype(str) + '_' +
        league_data['home_team'] + '_' +
        league_data['away_team']
    )
 
    league_data = league_data.rename(columns={
        'h_simu': 'home_predicted_goal',
        'a_simu': 'away_predicted_goal',
        'clean_h60': 'prehome',
        'clean_d60': 'predraw',
        'clean_a60': 'preaway'
    })
 
    # ============================================================================
    # STEP 3: CREATE MINUTE-BY-MINUTE DATASET (92 ROWS PER MATCH)
    # ============================================================================
 
    league_data_repeated = league_data.loc[league_data.index.repeat(92)].reset_index(drop=True)
    league_data_repeated['minute'] = np.tile(np.arange(1, 93), len(league_data))
 
    # ============================================================================
    # STEP 4: MERGE EMPIRICAL GOAL DISTRIBUTION
    # Multiply per-match scoring rates by the per-minute percentage to get
    # per-minute scoring probabilities for each team
    # ============================================================================
 
    goal_dist = pd.read_excel(GOAL_DIST_FILE)
 
    league_data_repeated = league_data_repeated.merge(
        goal_dist[['minute', 'percentage']],
        on='minute',
        how='left'
    )
 
    league_data_repeated['homescoring'] = (
        league_data_repeated['home_predicted_goal'] * league_data_repeated['percentage']
    )
    league_data_repeated['awayscoring'] = (
        league_data_repeated['away_predicted_goal'] * league_data_repeated['percentage']
    )
 
    # ============================================================================
    # STEP 5: MERGE GOALS AND RED CARDS
    # ============================================================================
 
    merged_data = league_data_repeated.merge(
        df_goals_reds,
        on='match_id',
        how='left'
    )
 
    # ============================================================================
    # DROP INTERMEDIATE ODDS AND RAW EVENT COLUMNS
    # ============================================================================
 
    cols_to_drop = [
        '0.5_over', '0.5_under', '1.5_over', '1.5_under',
        '2.5_over', '2.5_under', '3.5_over', '3.5_under',
        '4.5_over', '4.5_under', '5.5_over', '5.5_under',
        'recip_home', 'recip_draw', 'recip_away',
        '0.5under_recip', '0.5over_recip', '1.5under_recip', '1.5over_recip',
        '2.5under_recip', '2.5over_recip', '3.5under_recip', '3.5over_recip',
        '4.5under_recip', '4.5over_recip', '5.5under_recip', '5.5over_recip',
        'odd_sum_recips', '0.5_sum_recips', '1.5_sum_recips', '2.5_sum_recips',
        '3.5_sum_recips', '4.5_sum_recips', '5.5_sum_recips',
        'cav_ov05', 'cav_un05', 'cav_ov15', 'cav_un15',
        'cav_ov25', 'cav_un25', 'cav_ov35', 'cav_un35',
        'cav_ov45', 'cav_un45', 'cav_ov55', 'cav_un55',
        'Home_Team', 'Home_Goals', 'Home_Red_Cards',
        'Away_Team', 'Away_Goals', 'Away_Red_Cards',
        'Home_Away', 'Event_Time', 'Event_Half', 'Event_Type',
        'Matchup', 'ID'
    ]
 
    merged_data = merged_data.drop(
        columns=[c for c in cols_to_drop if c in merged_data.columns]
    )
 
    # ============================================================================
    # STEP 6: BUILD CUMULATIVE SCORE AND RED CARD COUNTERS
    # For each match, count cumulative goals and red cards up to each minute
    # ============================================================================
 
    merged_data['home_score_time'] = 0
    merged_data['away_score_time'] = 0
    merged_data['home_red_time']   = 0
    merged_data['away_red_time']   = 0
 
    homegoal_cols = [c for c in merged_data.columns if c.startswith('homegoal')]
    awaygoal_cols = [c for c in merged_data.columns if c.startswith('awaygoal')]
    homered_cols  = [c for c in merged_data.columns if c.startswith('homered')]
    awayred_cols  = [c for c in merged_data.columns if c.startswith('awayred')]
 
    def update_counter(group, event_cols, target_col):
        count = 0
        for idx, row in group.sort_values('minute').iterrows():
            for c in event_cols:
                if pd.notnull(row[c]) and row['minute'] == row[c]:
                    count += 1
            group.at[idx, target_col] = count
        return group
 
    for cols, tgt in [
        (homegoal_cols, 'home_score_time'),
        (awaygoal_cols, 'away_score_time'),
        (homered_cols,  'home_red_time'),
        (awayred_cols,  'away_red_time'),
    ]:
        merged_data = merged_data.groupby(
            'odds_matchdate_id', group_keys=False
        ).apply(lambda g: update_counter(g, cols, tgt))
 
    merged_data['score'] = (
        merged_data['home_score_time'].astype(str) + "," +
        merged_data['away_score_time'].astype(str)
    )
    merged_data['red'] = (
        merged_data['home_red_time'].astype(str) + "," +
        merged_data['away_red_time'].astype(str)
    )
 
    # ============================================================================
    # SAVE OUTPUT
    # ============================================================================
 
    Path(OUTPUT_FILE).parent.mkdir(parents=True, exist_ok=True)
    merged_data.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")
 
    print(" Processing complete")
    print(f"   Total rows:    {len(merged_data):,}")
    print(f"   Total matches: {merged_data['match_id'].nunique()}")
    print(f"   Output file:   {OUTPUT_FILE}")
 
    return merged_data
 
 
if __name__ == "__main__":
    process_league_data()
 