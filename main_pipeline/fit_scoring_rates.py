# ============================================================================
# FIT SCORING RATES
# ============================================================================
# This script fits Poisson-based scoring rates (lambda values) to cleaned
# bookmaker odds for each match using a grid search approach. For each match,
# it finds the home and away scoring rate combination that best explains the
# observed over/under and match result odds.
#
# INPUT:  Cleaned odds CSV file (output of clean_bookmaker_odds.py)
# OUTPUT: CSV file with predicted home and away scoring rates appended
# ============================================================================
 
import pandas as pd
import numpy as np
from scipy.stats import poisson
 
# ============================================================================
# SETTINGS — EDIT THESE FOR YOUR LEAGUE
# ============================================================================
 
INPUT_FILE  = r"path/to/your/clean_odds.csv"
OUTPUT_FILE = r"path/to/your/predicted_goals.csv"
 
# ============================================================================
# FUNCTIONS
# ============================================================================
 
def score_lines_per_match(lam):
    """
    Given lam = [lamA, lamB], return a 10x10 matrix with probabilities
    for each (i, j) scoreline using independent Poisson distributions.
    """
    goals = poisson(lam)
    x = np.zeros([10, 10])
    for i in range(0, x.shape[0]):
        for j in range(0, x.shape[1]):
            x[i, j] = goals.pmf([i, j])[0] * goals.pmf([i, j])[1]
    return x
 
def float_range(A, L=None, D=None):
    """Float-based range generator."""
    if L is None:
        L = A + 0.0
        A = 0.0
    if D is None:
        D = 1.0
    while True:
        if D > 0 and A >= L:
            break
        elif D < 0 and A <= L:
            break
        yield ("%g" % A)
        A = A + D
 
# ============================================================================
# PRECOMPUTE POISSON PROBABILITIES FOR ALL LAMBDA PAIRS
# ============================================================================
 
lamdas_a = []
lamdas_b = []
for i in float_range(0, 6, 0.1):
    lamdas_a.append(float(i))
    lamdas_b.append(float(i))
 
mega = []
for x in lamdas_a:
    for y in lamdas_b:
        mega.append([x, y])
 
keep_stats = {}
for lam_pair in mega:
    x = score_lines_per_match(lam_pair)
    dff = pd.DataFrame(x)
 
    totalAway = sum([x[i][j] for i in range(1, x.shape[0]) for j in range(i)])
    totalHome = sum([x[i][j] for i in range(x.shape[0]) for j in range(i+1, x.shape[1])])
    total_draw = dff.values.sum() - totalAway - totalHome
 
    under_5  = x[0][0]
    over_5   = dff.values.sum() - under_5
    under_15 = under_5 + x[1][0] + x[0][1]
    over_15  = dff.values.sum() - under_15
    under_25 = under_15 + x[2][0] + x[0][2] + x[1][1]
    over_25  = dff.values.sum() - under_25
    under_35 = under_25 + x[3][0] + x[0][3] + x[2][1] + x[1][2]
    over_35  = dff.values.sum() - under_35
    under_45 = under_35 + x[4][0] + x[3][1] + x[2][2] + x[1][3] + x[0][4]
    over_45  = dff.values.sum() - under_45
    under_55 = under_45 + x[5][0] + x[4][1] + x[3][2] + x[2][3] + x[1][4] + x[0][5]
    over_55  = dff.values.sum() - under_55
 
    keep_stats[f'{lam_pair[0]:.1f}_{lam_pair[1]:.1f}'] = [
        under_5, under_15, under_25, under_35, under_45, under_55,
        over_5,  over_15,  over_25,  over_35,  over_45,  over_55,
        totalHome, totalAway, total_draw
    ]
 
# ============================================================================
# READ MATCH DATA
# ============================================================================
 
df = pd.read_csv(INPUT_FILE)
 
column_map = {
    'cav_un05': 0,  'cav_un15': 1,  'cav_un25': 2,
    'cav_un35': 3,  'cav_un45': 4,  'cav_un55': 5,
    'cav_ov05': 6,  'cav_ov15': 7,  'cav_ov25': 8,
    'cav_ov35': 9,  'cav_ov45': 10, 'cav_ov55': 11,
    'clean_h60': 12, 'clean_a60': 13, 'clean_d60': 14
}
 
lists_dict = {}
for col in column_map.keys():
    if col in df.columns:
        lists_dict[col] = df[col].astype(float).to_list()
    else:
        lists_dict[col] = None
 
# ============================================================================
# GRID SEARCH — FIND BEST FITTING LAMBDA PAIR PER MATCH
# ============================================================================
 
lamdaz = []
paul_bearer = []
 
num_rows = len(df)
for row_idx in range(num_rows):
    min_track = []
    lamda_track = {}
 
    for lam_key, stats_list in keep_stats.items():
        sse = 0.0
        for col, stat_idx in column_map.items():
            if lists_dict[col] is not None:
                value = lists_dict[col][row_idx]
                if not pd.isnull(value):
                    diff = value - stats_list[stat_idx]
                    sse += diff**2
 
        min_track.append(sse)
        lamda_track[sse] = lam_key
 
    min_val = min(min_track)
    paul_bearer.append(min_val)
    lamdaz.append(lamda_track[min_val])
 
# ============================================================================
# EXTRACT PREDICTED SCORING RATES AND SAVE
# ============================================================================
 
home_log = []
away_log = []
 
for lam_str in lamdaz:
    away_score_str, home_score_str = lam_str.split("_")
    away_log.append(float(away_score_str))
    home_log.append(float(home_score_str))
 
df['h_simu'] = home_log
df['a_simu'] = away_log
 
df.to_csv(OUTPUT_FILE, index=False)
print(f"Predicted scoring rates saved to: {OUTPUT_FILE}")