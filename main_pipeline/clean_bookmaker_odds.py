# ============================================================================
# CLEAN BOOKMAKER ODDS (REMOVE OVERROUND)
# ============================================================================
# This script converts raw bookmaker odds into true implied probabilities
# by removing the overround (bookmaker margin). It processes both the
# match result odds (home/draw/away) and over/under goal line odds (0.5-5.5).
#
# INPUT:  Raw bookmaker odds file (one row per match)
# OUTPUT: Cleaned odds file with implied probabilities appended
# ============================================================================

import pandas as pd

# ============================================================================
# SETTINGS — EDIT THESE FOR YOUR LEAGUE/SEASON
# ============================================================================

INPUT_FILE  = r"path/to/your/raw_odds.xlsx"
OUTPUT_FILE = r"path/to/your/clean_odds.xlsx"

# Column names for home/draw/away closing odds in your input file
HOME_ODDS_COL = '1_Closing'
DRAW_ODDS_COL = 'X_Closing'
AWAY_ODDS_COL = '2_Closing'

# Column index range for over/under odds (0-based, e.g. columns 12 to 24)
OU_COLS_START = 12
OU_COLS_END   = 24

# ============================================================================
# LOAD DATA
# ============================================================================

data = pd.read_excel(INPUT_FILE)

# ============================================================================
# CONVERT OVER/UNDER COLUMNS TO FLOAT
# ============================================================================

columns_to_convert = data.columns[OU_COLS_START:OU_COLS_END]
for col in columns_to_convert:
    data[col] = pd.to_numeric(data[col], errors='coerce')

# ============================================================================
# CALCULATE RECIPROCALS
# ============================================================================

# Match result odds
data['recip_home'] = 1 / data[HOME_ODDS_COL]
data['recip_draw'] = 1 / data[DRAW_ODDS_COL]
data['recip_away'] = 1 / data[AWAY_ODDS_COL]

# Over/under odds
for threshold in ['0.5', '1.5', '2.5', '3.5', '4.5', '5.5']:
    data[f'{threshold}under_recip'] = 1 / data[f'{threshold}_UNDER']
    data[f'{threshold}over_recip']  = 1 / data[f'{threshold}_OVER']

# ============================================================================
# CALCULATE SUM OF RECIPROCALS (OVERROUND)
# ============================================================================

data['odd_sum_recips'] = (data['recip_home'] +
                          data['recip_draw'] +
                          data['recip_away'])

for threshold in ['0.5', '1.5', '2.5', '3.5', '4.5', '5.5']:
    data[f'{threshold}_sum_recips'] = (data[f'{threshold}under_recip'] +
                                       data[f'{threshold}over_recip'])

# ============================================================================
# CALCULATE CLEAN PROBABILITIES (OVERROUND REMOVED)
# ============================================================================

data['clean_h60'] = data['recip_home'] / data['odd_sum_recips']
data['clean_d60'] = data['recip_draw'] / data['odd_sum_recips']
data['clean_a60'] = data['recip_away'] / data['odd_sum_recips']

for threshold in ['0.5', '1.5', '2.5', '3.5', '4.5', '5.5']:
    data[f'cav_ov{threshold.replace(".", "")}'] = (
        data[f'{threshold}over_recip'] / data[f'{threshold}_sum_recips']
    )
    data[f'cav_un{threshold.replace(".", "")}'] = (
        data[f'{threshold}under_recip'] / data[f'{threshold}_sum_recips']
    )

# ============================================================================
# SAVE OUTPUT
# ============================================================================

data.to_excel(OUTPUT_FILE, index=False)
print(f"Clean odds file saved to: {OUTPUT_FILE}")