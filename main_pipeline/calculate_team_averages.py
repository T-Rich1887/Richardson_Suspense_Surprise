# ============================================================================
# CALCULATE TEAM AVERAGES
# ============================================================================
# This script calculates season-by-season average suspense and surprise
# for a set of focus teams in each league, plus an "Other" group covering
# all games not involving any of the focus teams.
#
# For each league, focus teams are the three most prominent clubs. All games
# involving a focus team (home or away) are included in that team's group.
# Games not involving any focus team are grouped as "Other".
#
# Run this script once per league by uncommenting the appropriate settings
# block and commenting out the others.
#
# INPUT:  Game-level results Excel file (output of calculate_league_averages.py,
#         Game_Results sheet)
# OUTPUT: Excel file with season averages per team group
# ============================================================================
 
import pandas as pd
 
# ============================================================================
# SETTINGS - UNCOMMENT THE BLOCK FOR YOUR LEAGUE
# ============================================================================
 
# --- EPL (England) ---
INPUT_FILE   = r"path/to/England_Men/Final/EPL_Final_season_averages.xlsx"
OUTPUT_FILE  = r"path/to/England_Men/Final/EPL_Final_team_averages.xlsx"
FOCUS_TEAMS  = ['Manchester City', 'Arsenal', 'Liverpool']
 
# --- Ligue 1 (France) ---
# INPUT_FILE   = r"path/to/France_Men/Final/Ligue1_Final_season_averages.xlsx"
# OUTPUT_FILE  = r"path/to/France_Men/Final/Ligue1_Final_team_averages.xlsx"
# FOCUS_TEAMS  = ['Paris Saint-Germain', 'Lyon', 'Marseille']
 
# --- Bundesliga (Germany) ---
# INPUT_FILE   = r"path/to/Germany_Men/Final/Bundesliga_Final_season_averages.xlsx"
# OUTPUT_FILE  = r"path/to/Germany_Men/Final/Bundesliga_Final_team_averages.xlsx"
# FOCUS_TEAMS  = ['Bayern Munich', 'Dortmund', 'Bayer Leverkusen']
 
# --- Serie A (Italy) ---
# INPUT_FILE   = r"path/to/Italy_Men/Final/SerieA_Final_season_averages.xlsx"
# OUTPUT_FILE  = r"path/to/Italy_Men/Final/SerieA_Final_team_averages.xlsx"
# FOCUS_TEAMS  = ['Juventus', 'Napoli', 'Internazionale']
 
# --- La Liga (Spain) ---
# INPUT_FILE   = r"path/to/Spain_Men/Final/LaLiga_Final_season_averages.xlsx"
# OUTPUT_FILE  = r"path/to/Spain_Men/Final/LaLiga_Final_team_averages.xlsx"
# FOCUS_TEAMS  = ['Real Madrid', 'Barcelona', 'Atlético Madrid']
 
# ============================================================================
# LOAD GAME-LEVEL DATA
# ============================================================================
 
games = pd.read_excel(INPUT_FILE, sheet_name='Game_Results')
 
# Extract home and away teams from match_id (format: YYYY_HomeTeam_AwayTeam)
teams_split     = games['match_id'].str.split('_', n=2, expand=True)
games['home_team'] = teams_split[1]
games['away_team'] = teams_split[2]
 
# ============================================================================
# CALCULATE SEASON AVERAGES PER TEAM GROUP
# ============================================================================
 
results = []
 
# --- Focus teams ---
for team in FOCUS_TEAMS:
    team_games = games[
        (games['home_team'] == team) | (games['away_team'] == team)
    ]
    season_avgs = (
        team_games
        .groupby('season')[['suspense', 'surprise', 'suspense_z', 'surprise_z']]
        .mean()
        .reset_index()
    )
    season_avgs['team_group'] = team
    results.append(season_avgs)
 
# --- Other teams (no games involving any focus team) ---
mask_other = ~games.apply(
    lambda row: any(
        row['home_team'] == t or row['away_team'] == t
        for t in FOCUS_TEAMS
    ),
    axis=1
)
other_games = games[mask_other]
other_season_avgs = (
    other_games
    .groupby('season')[['suspense', 'surprise', 'suspense_z', 'surprise_z']]
    .mean()
    .reset_index()
)
other_season_avgs['team_group'] = 'Other'
results.append(other_season_avgs)
 
# ============================================================================
# COMBINE AND SAVE
# ============================================================================
 
final_df = pd.concat(results, ignore_index=True)
 
final_df = final_df[[
    'team_group', 'season',
    'suspense', 'surprise',
    'suspense_z', 'surprise_z'
]]
 
final_df.to_excel(OUTPUT_FILE, index=False)
 
print(f" Team averages saved to:\n{OUTPUT_FILE}")