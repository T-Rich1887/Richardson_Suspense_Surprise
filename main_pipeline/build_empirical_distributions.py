# ============================================================================
# BUILD EMPIRICAL GOAL AND RED CARD DISTRIBUTIONS
# ============================================================================
# This script processes all season goals/reds files for a league and builds
# the empirical minute-by-minute distributions for goals and red cards.
# These distributions are used in the main pipeline to scale per-match
# scoring rates into per-minute scoring probabilities.
#
# The script runs three steps in sequence:
#   1. Extract goal and red card minutes from each season file
#   2. Combine all seasons into one file
#   3. Build the final empirical distributions (one for goals, one for reds)
#
# INPUT:  Folder of cleaned goals/reds files (one per season)
# OUTPUT: Two CSV files:
#           - empirical_goal_distribution.csv (minute 1-92, count, percentage)
#           - empirical_red_distribution.csv  (minute 1-92, count, percentage)
# ============================================================================

import pandas as pd
from pathlib import Path
 
# ============================================================================
# SETTINGS - EDIT THESE FOR YOUR LEAGUE
# ============================================================================
 
GOALS_REDS_DIR = Path(r"path/to/your/goals_reds_output")
OUTPUT_DIR     = Path(r"path/to/your/Goal_Distribution")
LEAGUE_NAME    = "YourLeague"   # e.g. "EPL", "Bundesliga", "LaLiga"
 
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
 
# ============================================================================
# HELPER FUNCTIONS
# ============================================================================
 
def stack_minutes(df, cols, col_name):
    """Melts wide-format goal/red columns into a single column of minutes."""
    out = (
        df[cols]
        .melt(value_name=col_name)
        .dropna(subset=[col_name])
    )
    out[col_name] = out[col_name].astype(int)
    return out[[col_name]].reset_index(drop=True)
 
 
def build_empirical_distribution(series):
    """Builds a minute-by-minute distribution from a series of event minutes."""
    series = series.dropna().astype(int)
    total  = len(series)
    counts = (
        series
        .value_counts()
        .reindex(range(1, 93), fill_value=0)
        .sort_index()
    )
    return pd.DataFrame({
        "minute":     counts.index,
        "count":      counts.values,
        "percentage": counts.values / total if total > 0 else 0
    })
 
 
# ============================================================================
# STEP 1: EXTRACT GOAL AND RED CARD MINUTES FROM EACH SEASON FILE
# ============================================================================
 
print("Step 1: Extracting goal and red card minutes from season files...")
 
season_files = sorted(GOALS_REDS_DIR.glob("*_goals_reds.csv"))
print(f"Found {len(season_files)} season files")
 
season_dfs = []
 
for file in season_files:
    print(f"  Processing {file.name}")
    df = pd.read_csv(file)
 
    home_goal_cols = [c for c in df.columns if c.startswith("homegoal")]
    away_goal_cols = [c for c in df.columns if c.startswith("awaygoal")]
    home_red_cols  = [c for c in df.columns if c.startswith("homered")]
    away_red_cols  = [c for c in df.columns if c.startswith("awayred")]
 
    home_goals = stack_minutes(df, home_goal_cols, "home_goal_minute")
    away_goals = stack_minutes(df, away_goal_cols, "away_goal_minute")
    home_reds  = stack_minutes(df, home_red_cols,  "home_red_minute")
    away_reds  = stack_minutes(df, away_red_cols,  "away_red_minute")
 
    all_goals = pd.concat(
        [
            home_goals.rename(columns={"home_goal_minute": "all_goal_minute"}),
            away_goals.rename(columns={"away_goal_minute": "all_goal_minute"})
        ],
        ignore_index=True
    )
    all_reds = pd.concat(
        [
            home_reds.rename(columns={"home_red_minute": "all_red_minute"}),
            away_reds.rename(columns={"away_red_minute": "all_red_minute"})
        ],
        ignore_index=True
    )
 
    max_len = max(
        len(home_goals), len(away_goals), len(all_goals),
        len(home_reds),  len(away_reds),  len(all_reds)
    )
 
    def pad(df, col):
        return df.reindex(range(max_len))[col]
 
    season_df = pd.DataFrame({
        "home_goal_minute": pad(home_goals, "home_goal_minute"),
        "away_goal_minute": pad(away_goals, "away_goal_minute"),
        "all_goal_minute":  pad(all_goals,  "all_goal_minute"),
        "home_red_minute":  pad(home_reds,  "home_red_minute"),
        "away_red_minute":  pad(away_reds,  "away_red_minute"),
        "all_red_minute":   pad(all_reds,   "all_red_minute"),
    })
 
    season_dfs.append(season_df)
    print(f"    -> {len(season_df)} rows extracted")
 
print("Step 1 complete!")
 
# ============================================================================
# STEP 2: COMBINE ALL SEASONS INTO ONE FILE
# ============================================================================
 
print("\nStep 2: Combining all seasons...")
 
combined_df = pd.concat(season_dfs, ignore_index=True)
 
combined_file = OUTPUT_DIR / f"{LEAGUE_NAME}_ALLSEASONS_empdist_goals_reds.csv"
combined_df.to_csv(combined_file, index=False)
 
print(f"  Combined file: {len(combined_df)} rows")
print(f"  Saved to: {combined_file}")
print("Step 2 complete!")
 
# ============================================================================
# STEP 3: BUILD EMPIRICAL DISTRIBUTIONS
# ============================================================================
 
print("\nStep 3: Building empirical distributions...")
 
goal_dist = build_empirical_distribution(combined_df["all_goal_minute"])
red_dist  = build_empirical_distribution(combined_df["all_red_minute"])
 
goal_output = OUTPUT_DIR / f"{LEAGUE_NAME}_ALLSEASONS_empirical_goal_distribution.csv"
red_output  = OUTPUT_DIR / f"{LEAGUE_NAME}_ALLSEASONS_empirical_red_distribution.csv"
 
goal_dist.to_csv(goal_output, index=False)
red_dist.to_csv(red_output, index=False)
 
print(f"  Goals: {goal_dist['count'].sum()} total across all minutes")
print(f"  Reds:  {red_dist['count'].sum()} total across all minutes")
print(f"  Saved: {goal_output}")
print(f"  Saved: {red_output}")
print("\nAll steps complete!")