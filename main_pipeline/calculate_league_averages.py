# ============================================================================
# CALCULATE LEAGUE AVERAGES
# ============================================================================
# This script takes the final minute-by-minute suspense and surprise output
# for each league and produces two outputs:
#   1. Game-level results: total suspense and surprise per match with
#      global z-scores normalised across all seasons in that league
#   2. Season averages: mean suspense, surprise and z-scores per season
#
# Run this script once per league by updating the three settings below.
#
# INPUT:  Surprise output CSV (output of calculate_surprise_shock.py)
# OUTPUT: Excel file with two sheets — Game_Results and Season_Averages
# ============================================================================
 
import pandas as pd
import os
 
# ============================================================================
# SETTINGS - EDIT THESE FOR YOUR LEAGUE
# ============================================================================
 
INPUT_FILE  = r"path/to/your/Surprise/League_Surprise.csv"
OUTPUT_DIR  = r"path/to/your/Final"
OUTPUT_FILE = "League_Final_season_averages.xlsx"
 
os.makedirs(OUTPUT_DIR, exist_ok=True)
OUTPUT_PATH = os.path.join(OUTPUT_DIR, OUTPUT_FILE)
 
# ============================================================================
# LOAD DATA
# ============================================================================
 
df = pd.read_csv(INPUT_FILE)
df.sort_values(by=['odds_matchdate_id', 'minute'], inplace=True)
 
# ============================================================================
# SHEET 1: GAME-LEVEL RESULTS
# Sum suspense and surprise over all 92 minutes per game, then add
# global z-scores normalised across all seasons in the league
# ============================================================================
 
grouped = df.groupby('odds_matchdate_id')
 
game_sums = grouped[['suspense', 'surprise']].sum().reset_index()
 
final_info = grouped.apply(
    lambda x: x.iloc[-1][['match_id', 'season', 'score']]
).reset_index()
final_info.rename(columns={'score': 'final_score'}, inplace=True)
 
game_results = game_sums.merge(final_info, on='odds_matchdate_id')
 
# Global z-score normalisation across all seasons
game_results['suspense_z'] = (
    (game_results['suspense'] - game_results['suspense'].mean()) /
    game_results['suspense'].std()
)
game_results['surprise_z'] = (
    (game_results['surprise'] - game_results['surprise'].mean()) /
    game_results['surprise'].std()
)
 
game_results = game_results[[
    'odds_matchdate_id', 'match_id', 'season',
    'suspense', 'surprise', 'suspense_z', 'surprise_z',
    'final_score'
]]
 
# ============================================================================
# SHEET 2: SEASON AVERAGES
# ============================================================================
 
season_averages = (
    game_results
    .groupby('season')[['suspense', 'surprise', 'suspense_z', 'surprise_z']]
    .mean()
    .reset_index()
)
season_averages.rename(columns={
    'suspense':   'average_suspense',
    'surprise':   'average_surprise',
    'suspense_z': 'average_suspense_z',
    'surprise_z': 'average_surprise_z'
}, inplace=True)
 
# ============================================================================
# SAVE
# ============================================================================
 
with pd.ExcelWriter(OUTPUT_PATH, engine='xlsxwriter') as writer:
    game_results.to_excel(writer,    sheet_name='Game_Results',    index=False)
    season_averages.to_excel(writer, sheet_name='Season_Averages', index=False)
 
print(f"League averages saved to:\n{OUTPUT_PATH}")