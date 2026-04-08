# ============================================================================
# FIX SPECIFIC MATCH ERRORS
# ============================================================================
# This script fixes two specific data errors discovered during processing:
#
#   1. BUNDESLIGA 2015/16 - Wrong season year:
#      The match Bayern Munich vs Werder Bremen was assigned to season 1516
#      but odds_matchdate_id 2448 was incorrectly labelled as 2015 instead
#      of 2016. This fix corrects the match_id and season for those rows.
#
#   2. SERIE A - Playoff game not deleted:
#      A playoff match was incorrectly included in the Serie A dataset
#      (odds_matchdate_id == 381). This fix removes those 92 rows and
#      renumbers all odds_matchdate_id values to maintain sequential ordering.
#
# INPUT:  Raw minute-by-minute CSV files (output of build_minute_dataset.py)
# OUTPUT: Corrected CSV files
# ============================================================================
 
import pandas as pd
from pathlib import Path
 
# ============================================================================
# SETTINGS - UPDATE PATHS FOR YOUR SYSTEM
# ============================================================================
 
BL_INPUT   = r"path/to/Germany_Men/Clean_for_step3_output/Bundesliga_get_minute_betting_odds.csv"
BL_OUTPUT  = r"path/to/Germany_Men/Clean_for_step3_output/Bundesliga_get_minute_betting_odds_fixed.csv"
 
SA_INPUT   = r"path/to/Italy_Men/Clean_for_step3_output/SerieA_get_minute_betting_odds.csv"
SA_OUTPUT  = r"path/to/Italy_Men/Clean_for_step3_output/SerieA_get_minute_betting_odds_fixed.csv"
 
# ============================================================================
# FIX 1: BUNDESLIGA - WRONG SEASON YEAR
# odds_matchdate_id 2448 has match_id "2015_Bayern Munich_Werder Bremen"
# but should be "2016_Bayern Munich_Werder Bremen" (season 1617)
# ============================================================================
 
print("Fix 1: Bundesliga wrong season year...")
 
df_bl = pd.read_csv(BL_INPUT)
print(f"  Original rows: {len(df_bl)}")
 
mask = df_bl["odds_matchdate_id"] == 2448
print(f"  Rows to fix: {mask.sum()}")
 
df_bl.loc[mask, "match_id"] = "2016_Bayern Munich_Werder Bremen"
df_bl.loc[mask, "season"]   = 1617
 
df_bl.to_csv(BL_OUTPUT, index=False, encoding="utf-8-sig")
print(f"  Saved to: {BL_OUTPUT}")
print("  Fix 1 complete!")
 
# ============================================================================
# FIX 2: SERIE A - REMOVE PLAYOFF GAME AND RENUMBER
# odds_matchdate_id 381 is a playoff match that should not be in the dataset.
# After deletion, all odds_matchdate_id values are renumbered sequentially.
# ============================================================================
 
print("\nFix 2: Serie A playoff game removal...")
 
df_sa = pd.read_csv(SA_INPUT)
print(f"  Original rows: {len(df_sa)}")
 
df_sa = df_sa[df_sa["odds_matchdate_id"] != 381].copy()
print(f"  Rows after deletion: {len(df_sa)}")
 
# Renumber odds_matchdate_id sequentially (92 rows per game)
df_sa = df_sa.reset_index(drop=True)
df_sa["odds_matchdate_id"] = (df_sa.index // 92) + 1
 
print(f"  New max odds_matchdate_id: {df_sa['odds_matchdate_id'].max()}")
 
# Sanity check
rows_per_game = df_sa.groupby("odds_matchdate_id").size()
assert rows_per_game.nunique() == 1, "ERROR: Not all games have the same number of rows!"
assert rows_per_game.iloc[0] == 92, "ERROR: Games do not have exactly 92 rows!"
 
df_sa.to_csv(SA_OUTPUT, index=False, encoding="utf-8-sig")
print(f"  Saved to: {SA_OUTPUT}")
print("  Fix 2 complete!")
 
print("\n All specific match fixes applied!")