# ============================================================================
# COMBINE SEASON FILES
# ============================================================================
# This script combines all individual season goals/reds files into one
# single file for use in the main pipeline. Run this after all season
# files have been processed and any corrections applied.
#
# INPUT:  Folder of individual season goals/reds files
# OUTPUT: Single combined Excel file with all seasons
# ============================================================================
 
import pandas as pd
from pathlib import Path
 
# ============================================================================
# SETTINGS - EDIT THESE FOR YOUR LEAGUE
# ============================================================================
 
INPUT_DIR   = Path(r"path/to/your/goals_reds_output")
OUTPUT_FILE = INPUT_DIR / "YourLeague_allseasons_goals_reds.xlsx"
 
# ============================================================================
# FIND, COMBINE AND SAVE
# ============================================================================
 
files = sorted(INPUT_DIR.glob("*_*_goals_reds.xlsx"))
print(f"Found {len(files)} season files")
 
dfs = []
for file in files:
    print(f"  Reading {file.name}")
    dfs.append(pd.read_excel(file))
 
combined_df = pd.concat(dfs, ignore_index=True)
 
combined_df.to_excel(OUTPUT_FILE, index=False)
print(f"\n Combined file saved")
print(f"   Total rows: {len(combined_df)}")
print(f"   Saved to:   {OUTPUT_FILE}")
 