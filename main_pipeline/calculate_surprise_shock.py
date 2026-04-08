# ============================================================================
# CALCULATE SURPRISE AND SHOCK
# ============================================================================
# This script calculates two backward-looking emotion measures for each match:
#
#   SURPRISE: The Euclidean distance between outcome probability vectors at
#   consecutive minutes. It captures the immediate unexpectedness of changes
#   in live odds from one minute to the next.
#
#     SUR_t = sqrt(
#         (p_home_t - p_home_(t-1))^2 +
#         (p_draw_t - p_draw_(t-1))^2 +
#         (p_away_t - p_away_(t-1))^2
#     )
#
#   SHOCK: The Euclidean distance between current live odds and pre-match
#   closing odds. It captures the total deviation from pre-match expectations
#   at any point in the match.
#
#     SHO_t = sqrt(
#         (p_home_live_t - p_home_pre)^2 +
#         (p_draw_live_t - p_draw_pre)^2 +
#         (p_away_live_t - p_away_pre)^2
#     )
#
#   MINUTE 1 ADJUSTMENT: If a goal or red card occurs in minute 1, the
#   standard surprise formula cannot be applied (no previous minute exists).
#   In such cases, the shock value is substituted for surprise in minute 1
#   to capture the impact of those early events.
#
#   NOTE: Shock is calculated as an intermediate value only. It is not
#   retained as a standalone column in the output — it is used solely to
#   handle the minute 1 edge case described above.
#
# INPUT:  Suspense file (output of calculate_suspense.py)
# OUTPUT: Same dataset with surprise column appended
# ============================================================================
 
import pandas as pd
import numpy as np
import os
 
# ============================================================================
# SETTINGS - EDIT THESE FOR YOUR LEAGUE
# ============================================================================
 
INPUT_FILE  = r"path/to/your/suspense_output.csv"
OUTPUT_FILE = r"path/to/your/surprise_output.csv"
 
os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
 
# ============================================================================
# LOAD DATA
# ============================================================================
 
df = pd.read_csv(INPUT_FILE)
 
# Sort by game and minute to ensure correct diff calculations
df.sort_values(by=['odds_matchdate_id', 'minute'], inplace=True)
 
# ============================================================================
# SECTION 1: CALCULATE SURPRISE
# Minute-to-minute change in live outcome probabilities within each match
# ============================================================================
 
df['homeprobminus1'] = df.groupby('odds_matchdate_id')['clean_av_home'].diff()
df['drawprobminus1'] = df.groupby('odds_matchdate_id')['clean_av_draw'].diff()
df['awayprobminus1'] = df.groupby('odds_matchdate_id')['clean_av_away'].diff()
 
df['home_prob_sq'] = df['homeprobminus1'] ** 2
df['draw_prob_sq'] = df['drawprobminus1'] ** 2
df['away_prob_sq'] = df['awayprobminus1'] ** 2
 
df['surprise'] = np.sqrt(
    df['home_prob_sq'] +
    df['draw_prob_sq'] +
    df['away_prob_sq']
)
 
# First minute of each game has no previous minute — set to 0 by default
df['surprise'].fillna(0, inplace=True)
 
df.drop(columns=[
    'homeprobminus1', 'drawprobminus1', 'awayprobminus1',
    'home_prob_sq', 'draw_prob_sq', 'away_prob_sq'
], inplace=True)
 
# ============================================================================
# SECTION 2: CALCULATE SHOCK
# Total deviation from pre-match closing odds at each minute
# ============================================================================
 
df['homeprobminus0'] = df['clean_av_home'] - df['prehome']
df['drawprobminus0'] = df['clean_av_draw'] - df['predraw']
df['awayprobminus0'] = df['clean_av_away'] - df['preaway']
 
df['home_prob_sq'] = df['homeprobminus0'] ** 2
df['draw_prob_sq'] = df['drawprobminus0'] ** 2
df['away_prob_sq'] = df['awayprobminus0'] ** 2
 
df['shock'] = np.sqrt(
    df['home_prob_sq'] +
    df['draw_prob_sq'] +
    df['away_prob_sq']
)
 
df.drop(columns=[
    'homeprobminus0', 'drawprobminus0', 'awayprobminus0',
    'home_prob_sq', 'draw_prob_sq', 'away_prob_sq'
], inplace=True)
 
# ============================================================================
# SECTION 3: MINUTE 1 ADJUSTMENT
# If a goal or red card occurred in minute 1, substitute shock for surprise
# since there is no previous minute to calculate a standard surprise value
# ============================================================================
 
mask_min1_goal_red = (
    (df['minute'] == 1) &
    ((df['score'] != "0,0") | (df['red'] != "0,0"))
)
 
df.loc[mask_min1_goal_red, 'surprise'] = df.loc[mask_min1_goal_red, 'shock']
 
# Drop shock — used only for the minute 1 adjustment above
df.drop(columns=['shock'], inplace=True)
 
# ============================================================================
# SAVE OUTPUT
# ============================================================================
 
df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")
print(f"✅ Surprise file saved to:\n{OUTPUT_FILE}")