# ============================================================================
# CALCULATE DESCRIPTIVE STATISTICS
# ============================================================================
# This script calculates descriptive statistics for suspense and surprise
# across all five leagues. It runs four steps in sequence:
#
#   1. League-specific descriptives: mean, median, SD, min, max for raw
#      suspense and surprise and league-level z-scores, reported per league
#      and pooled across all leagues
#
#   2. Global z-score standardisation: computes z-scores using the grand
#      mean and SD pooled across all leagues combined
#
#   3. Global descriptives: same statistics as step 1 but using the global
#      z-scores, reported per league and pooled
#
#   4. Goals and red card distributions: minute-by-minute counts of home,
#      away and total goals and red cards per league and combined
#
# INPUT:  - Game_Results sheet from calculate_league_averages.py (5 leagues)
#         - Empirical distribution files from build_empirical_distributions.py
# OUTPUT: Three Excel files saved to the output directories below
# ============================================================================
 
import pandas as pd
import numpy as np
import os
 
# ============================================================================
# SETTINGS - UPDATE PATHS FOR YOUR SYSTEM
# ============================================================================
 
LEAGUE_FILES = {
    "EPL":        r"path/to/England_Men/Final/EPL_Final_season_averages.xlsx",
    "Bundesliga": r"path/to/Germany_Men/Final/Bundesliga_Final_season_averages.xlsx",
    "LaLiga":     r"path/to/Spain_Men/Final/LaLiga_Final_season_averages.xlsx",
    "SerieA":     r"path/to/Italy_Men/Final/SerieA_Final_season_averages.xlsx",
    "Ligue1":     r"path/to/France_Men/Final/Ligue1_Final_season_averages.xlsx",
}
 
DIST_FILES = {
    "EPL":        r"path/to/England_Men/Goal_Distribution/EPL_ALLSEASONS_empdist_goals_reds.xlsx",
    "Bundesliga": r"path/to/Germany_Men/Goal_Distribution/Bundesliga_ALLSEASONS_empdist_goals_reds.xlsx",
    "LaLiga":     r"path/to/Spain_Men/Goal_Distribution/LaLiga_ALLSEASONS_empdist_goals_reds.xlsx",
    "SerieA":     r"path/to/Italy_Men/Goal_Distribution/SerieA_ALLSEASONS_empdist_goals_reds.xlsx",
    "Ligue1":     r"path/to/France_Men/Goal_Distribution/Ligue1_ALLSEASONS_empdist_goals_reds.xlsx",
}
 
DESCRIPTIVES_OUTPUT = r"path/to/Descriptives/Suspense_Surprise_Descriptives.xlsx"
GLOBAL_OUTPUT       = r"path/to/All_Leagues/global_descriptives.xlsx"
DIST_OUTPUT         = r"path/to/All_Leagues/allLeagues_goals_red_distribution_halves.xlsx"
 
os.makedirs(os.path.dirname(DESCRIPTIVES_OUTPUT), exist_ok=True)
os.makedirs(os.path.dirname(GLOBAL_OUTPUT),        exist_ok=True)
os.makedirs(os.path.dirname(DIST_OUTPUT),           exist_ok=True)
 
# ============================================================================
# HELPER: COMPUTE DESCRIPTIVE STATISTICS
# ============================================================================
 
def compute_stats(df, label, z_suffix='z'):
    sus_z = f'suspense_{z_suffix}'
    sur_z = f'surprise_{z_suffix}'
    return {
        "Group":              label,
        "Total_Games":        len(df),
        "Suspense_Mean":      df["suspense"].mean(),
        "Suspense_Median":    df["suspense"].median(),
        "Suspense_SD":        df["suspense"].std(),
        "Suspense_Min":       df["suspense"].min(),
        "Suspense_Max":       df["suspense"].max(),
        "Surprise_Mean":      df["surprise"].mean(),
        "Surprise_Median":    df["surprise"].median(),
        "Surprise_SD":        df["surprise"].std(),
        "Surprise_Min":       df["surprise"].min(),
        "Surprise_Max":       df["surprise"].max(),
        "Suspense_Z_Mean":    df[sus_z].mean()   if sus_z in df.columns else np.nan,
        "Suspense_Z_Median":  df[sus_z].median() if sus_z in df.columns else np.nan,
        "Suspense_Z_SD":      df[sus_z].std()    if sus_z in df.columns else np.nan,
        "Suspense_Z_Min":     df[sus_z].min()    if sus_z in df.columns else np.nan,
        "Suspense_Z_Max":     df[sus_z].max()    if sus_z in df.columns else np.nan,
        "Surprise_Z_Mean":    df[sur_z].mean()   if sur_z in df.columns else np.nan,
        "Surprise_Z_Median":  df[sur_z].median() if sur_z in df.columns else np.nan,
        "Surprise_Z_SD":      df[sur_z].std()    if sur_z in df.columns else np.nan,
        "Surprise_Z_Min":     df[sur_z].min()    if sur_z in df.columns else np.nan,
        "Surprise_Z_Max":     df[sur_z].max()    if sur_z in df.columns else np.nan,
    }
 
# ============================================================================
# STEP 1: LOAD ALL LEAGUE FILES AND COMPUTE LEAGUE-SPECIFIC DESCRIPTIVES
# ============================================================================
 
print("Step 1: Computing league-specific descriptives...")
 
league_stats = []
all_games    = []
 
for league, path in LEAGUE_FILES.items():
    df           = pd.read_excel(path, sheet_name="Game_Results")
    df["league"] = league
    league_stats.append(compute_stats(df, league))
    all_games.append(df)
    print(f"  Loaded {league}: {len(df)} games")
 
league_summary_df = pd.DataFrame(league_stats).round(4)
 
pooled_df         = pd.concat(all_games, ignore_index=True)
pooled_summary_df = pd.DataFrame([compute_stats(pooled_df, "All_Leagues_Combined")]).round(4)
 
with pd.ExcelWriter(DESCRIPTIVES_OUTPUT, engine="xlsxwriter") as writer:
    league_summary_df.to_excel(writer, sheet_name="By_League",          index=False)
    pooled_summary_df.to_excel(writer, sheet_name="All_Leagues_Pooled", index=False)
 
print(f"  Saved to: {DESCRIPTIVES_OUTPUT}")
print("Step 1 complete!")
 
# ============================================================================
# STEP 2: GLOBAL Z-SCORE STANDARDISATION
# Compute z-scores using the grand mean and SD pooled across all leagues
# ============================================================================
 
print("\nStep 2: Computing global z-scores...")
 
suspense_mean_global = pooled_df["suspense"].mean()
suspense_sd_global   = pooled_df["suspense"].std()
surprise_mean_global = pooled_df["surprise"].mean()
surprise_sd_global   = pooled_df["surprise"].std()
 
pooled_df["suspense_z_global"] = (
    (pooled_df["suspense"] - suspense_mean_global) / suspense_sd_global
)
pooled_df["surprise_z_global"] = (
    (pooled_df["surprise"] - surprise_mean_global) / surprise_sd_global
)
 
print(f"  Global suspense mean: {suspense_mean_global:.4f}, SD: {suspense_sd_global:.4f}")
print(f"  Global surprise mean: {surprise_mean_global:.4f}, SD: {surprise_sd_global:.4f}")
print("Step 2 complete!")
 
# ============================================================================
# STEP 3: GLOBAL DESCRIPTIVES
# ============================================================================
 
print("\nStep 3: Computing global descriptives...")
 
global_league_rows = []
for league in pooled_df["league"].unique():
    league_df = pooled_df[pooled_df["league"] == league]
    global_league_rows.append(compute_stats(league_df, league, z_suffix='z_global'))
 
global_by_league_df  = pd.DataFrame(global_league_rows).round(4)
global_pooled_df     = pd.DataFrame([
    compute_stats(pooled_df, "All_Leagues_Combined", z_suffix='z_global')
]).round(4)
 
with pd.ExcelWriter(GLOBAL_OUTPUT, engine="xlsxwriter") as writer:
    global_by_league_df.to_excel(writer, sheet_name="By_League",          index=False)
    global_pooled_df.to_excel(writer,    sheet_name="All_Leagues_Pooled", index=False)
 
print(f"  Saved to: {GLOBAL_OUTPUT}")
print("Step 3 complete!")
 
# ============================================================================
# STEP 4: GOALS AND RED CARD DISTRIBUTIONS
# ============================================================================
 
print("\nStep 4: Computing goals and red card distributions...")
 
def build_minute_counts(df):
    minutes = list(range(1, 93))
    out     = pd.DataFrame({"minute": minutes})
    out["home_goals"]  = df["home_goal_minute"].value_counts().reindex(minutes, fill_value=0).values
    out["away_goals"]  = df["away_goal_minute"].value_counts().reindex(minutes, fill_value=0).values
    out["total_goals"] = df["all_goal_minute"].value_counts().reindex(minutes, fill_value=0).values
    out["home_reds"]   = df["home_red_minute"].value_counts().reindex(minutes, fill_value=0).values
    out["away_reds"]   = df["away_red_minute"].value_counts().reindex(minutes, fill_value=0).values
    out["total_reds"]  = df["all_red_minute"].value_counts().reindex(minutes, fill_value=0).values
    return out
 
def add_total_row(df):
    total_row = {
        "minute":      "Total",
        "home_goals":  df["home_goals"].sum(),
        "away_goals":  df["away_goals"].sum(),
        "total_goals": df["total_goals"].sum(),
        "home_reds":   df["home_reds"].sum(),
        "away_reds":   df["away_reds"].sum(),
        "total_reds":  df["total_reds"].sum(),
    }
    return pd.concat([df, pd.DataFrame([total_row])], ignore_index=True)
 
league_sheets = {}
combined_dist = None
 
for league, path in DIST_FILES.items():
    print(f"  Processing {league}...")
    df             = pd.read_excel(path)
    league_dist_df = build_minute_counts(df)
    league_dist_df = add_total_row(league_dist_df)
    league_sheets[league] = league_dist_df.copy()
 
    numeric_part = league_dist_df.iloc[:-1].copy()
    if combined_dist is None:
        combined_dist = numeric_part.copy()
    else:
        combined_dist.iloc[:, 1:] += numeric_part.iloc[:, 1:]
 
combined_dist = add_total_row(combined_dist)
 
with pd.ExcelWriter(DIST_OUTPUT, engine="xlsxwriter") as writer:
    combined_dist.to_excel(writer, sheet_name="All_Leagues_Combined", index=False)
    for league, df in league_sheets.items():
        df.to_excel(writer, sheet_name=league, index=False)
 
print(f"  Saved to: {DIST_OUTPUT}")
print("Step 4 complete!")
 
print("\n✅ All descriptive statistics complete!")