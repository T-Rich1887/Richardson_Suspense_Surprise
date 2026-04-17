# ============================================================================
# BUILD PLOTTING FILE
# ============================================================================
# This script merges game-level results with season-level team averages
# into a single wide-format file ready for plotting. It produces one output
# file per league containing individual game results alongside the seasonal
# average suspense and surprise for each focus team and the "Other" group.
#
# Run this script once per league by setting the LEAGUE variable below.
#
# INPUT:  - Game_Results sheet from calculate_league_averages.py output
#         - Team averages file from calculate_team_averages.py output
# OUTPUT: Single wide-format CSV file ready for plot_league_figures.py
# ============================================================================
 
import pandas as pd
import os
 
# ============================================================================
# SETTINGS - SET YOUR LEAGUE HERE
# ============================================================================
 
LEAGUE = "EPL"   # Options: "EPL", "Ligue1", "Bundesliga", "SerieA", "LaLiga"
 
# ============================================================================
# LEAGUE CONFIGURATIONS
# ============================================================================
 
LEAGUE_CONFIG = {
    "EPL": {
        "game_file":    r"path/to/England_Men/Final/EPL_Final_season_averages.xlsx",
        "team_file":    r"path/to/England_Men/Final/EPL_Final_team_averages.csv",
        "output_file":  r"path/to/England_Men/Final/EPL_Final_plotting_file.csv",
        "focus_teams": {
            "Manchester City": "city",
            "Arsenal":         "arsenal",
            "Liverpool":       "liverpool",
        },
    },
    "Ligue1": {
        "game_file":    r"path/to/France_Men/Final/Ligue1_Final_season_averages.xlsx",
        "team_file":    r"path/to/France_Men/Final/Ligue1_Final_team_averages.csv",
        "output_file":  r"path/to/France_Men/Final/Ligue1_Final_plotting_file.csv",
        "focus_teams": {
            "Paris Saint-Germain": "psg",
            "Lyon":                "lyon",
            "Marseille":           "marseille",
        },
    },
    "Bundesliga": {
        "game_file":    r"path/to/Germany_Men/Final/Bundesliga_Final_season_averages.xlsx",
        "team_file":    r"path/to/Germany_Men/Final/Bundesliga_Final_team_averages.csv",
        "output_file":  r"path/to/Germany_Men/Final/Bundesliga_Final_plotting_file.csv",
        "focus_teams": {
            "Bayern Munich":   "bayern",
            "Dortmund":        "dortmund",
            "Bayer Leverkusen": "leverkusen",
        },
    },
    "SerieA": {
        "game_file":    r"path/to/Italy_Men/Final/SerieA_Final_season_averages.xlsx",
        "team_file":    r"path/to/Italy_Men/Final/SerieA_Final_team_averages.csv",
        "output_file":  r"path/to/Italy_Men/Final/SerieA_Final_plotting_file.csv",
        "focus_teams": {
            "Juventus":       "juventus",
            "Napoli":         "napoli",
            "Internazionale": "inter",
        },
    },
    "LaLiga": {
        "game_file":    r"path/to/Spain_Men/Final/LaLiga_Final_season_averages.xlsx",
        "team_file":    r"path/to/Spain_Men/Final/LaLiga_Final_team_averages.csv",
        "output_file":  r"path/to/Spain_Men/Final/LaLiga_Final_plotting_file.csv",
        "focus_teams": {
            "Real Madrid":    "realmadrid",
            "Barcelona":      "barcelona",
            "Atlético Madrid": "atletico",
        },
    },
}
 
# ============================================================================
# LOAD CONFIG FOR SELECTED LEAGUE
# ============================================================================
 
config      = LEAGUE_CONFIG[LEAGUE]
focus_teams = config["focus_teams"]
team_map    = {**focus_teams, "Other": "other"}
 
# ============================================================================
# LOAD DATA
# ============================================================================
 
games     = pd.read_excel(config["game_file"], sheet_name="Game_Results")
team_avgs = pd.read_csv(config["team_file"])
 
# Extract home and away teams from match_id
teams_split        = games['match_id'].str.split('_', n=2, expand=True)
games['home_team'] = teams_split[1]
games['away_team'] = teams_split[2]
 
# ============================================================================
# PIVOT TEAM AVERAGES TO WIDE FORMAT
# ============================================================================
 
wide_rows = []
 
for season in games['season'].unique():
    row         = {'season': season}
    season_data = team_avgs[team_avgs['season'] == season]
 
    for team_name, prefix in team_map.items():
        team_row = season_data[season_data['team_group'] == team_name]
 
        if not team_row.empty:
            row[f'{prefix}_average_suspense']   = team_row['suspense'].values[0]
            row[f'{prefix}_average_surprise']   = team_row['surprise'].values[0]
            row[f'{prefix}_average_suspense_z'] = team_row['suspense_z'].values[0]
            row[f'{prefix}_average_surprise_z'] = team_row['surprise_z'].values[0]
        else:
            row[f'{prefix}_average_suspense']   = None
            row[f'{prefix}_average_surprise']   = None
            row[f'{prefix}_average_suspense_z'] = None
            row[f'{prefix}_average_surprise_z'] = None
 
    wide_rows.append(row)
 
season_wide = pd.DataFrame(wide_rows)
 
# ============================================================================
# MERGE INTO GAME-LEVEL DATA
# ============================================================================
 
final_df = games.merge(season_wide, on='season', how='left')
 
# ============================================================================
# DEFINE COLUMN ORDER
# ============================================================================
 
base_cols = [
    'odds_matchdate_id', 'match_id', 'season',
    'home_team', 'away_team', 'final_score',
    'suspense', 'surprise', 'suspense_z', 'surprise_z',
]
 
team_cols = []
for metric in ['suspense', 'surprise', 'suspense_z', 'surprise_z']:
    for prefix in team_map.values():
        team_cols.append(f'{prefix}_average_{metric}')
 
final_df = final_df[base_cols + team_cols]
 
# ============================================================================
# SAVE
# ============================================================================
 
final_df.to_csv(config["output_file"], index=False)
print(f" {LEAGUE} plotting file saved to:\n{config['output_file']}")