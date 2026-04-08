# ============================================================================
# INSERT MISSING MATCHES
# ============================================================================
# This script inserts 18 matches that were missing from the LaLiga 2023/24
# goals and reds file due to a data availability issue in the raw source.
# The goal and red card minutes for these matches were manually verified
# and hard-coded below.
#
# INPUT:  LaLiga 2023/24 goals/reds file (incomplete)
# OUTPUT: LaLiga 2023/24 goals/reds file with missing matches added
# ============================================================================
 
import pandas as pd
from pathlib import Path
 
# ============================================================================
# SETTINGS — UPDATE PATH FOR YOUR SYSTEM
# ============================================================================
 
BASE_DIR = Path(r"path/to/Spain_Men/goals_reds_output")
 
INPUT_FILE  = BASE_DIR / "LaLiga_20232024_goals_reds.xlsx"
OUTPUT_FILE = BASE_DIR / "LaLiga_20232024_goals_reds_FIXED.xlsx"
 
# ============================================================================
# MISSING MATCH DATA
# ============================================================================
 
MISSING_FIXES = [
    {"ID": 363, "year": 2023, "match_id": "2023_Almería_Cádiz",
     "homegoal1": 48, "homegoal2": 52, "homegoal3": 57,
     "homegoal4": 65, "homegoal5": 71, "homegoal6": 86,
     "awaygoal1": 30},
 
    {"ID": 364, "year": 2023, "match_id": "2023_Real Sociedad_Atlético Madrid",
     "awaygoal1": 9, "awaygoal2": 91, "awayred1": 91},
 
    {"ID": 365, "year": 2023, "match_id": "2023_Osasuna_Villarreal",
     "homegoal1": 30, "awaygoal1": 57},
 
    {"ID": 366, "year": 2023, "match_id": "2023_Girona_Granada",
     "homegoal1": 30, "homegoal2": 33, "homegoal3": 44,
     "homegoal4": 54, "homegoal5": 75, "homegoal6": 78, "homegoal7": 90,
     "awayred1": 61},
 
    {"ID": 367, "year": 2023, "match_id": "2023_Athletic Club_Sevilla",
     "homegoal1": 17, "homegoal2": 19},
 
    {"ID": 368, "year": 2023, "match_id": "2023_Atlético Madrid_Osasuna",
     "homegoal1": 55,
     "awaygoal1": 26, "awaygoal2": 52, "awaygoal3": 64, "awaygoal4": 88},
 
    {"ID": 369, "year": 2023, "match_id": "2023_Barcelona_Rayo Vallecano",
     "homegoal1": 3, "homegoal2": 72, "homegoal3": 75},
 
    {"ID": 370, "year": 2023, "match_id": "2023_Real Betis_Real Sociedad",
     "awaygoal1": 5, "awaygoal2": 42},
 
    {"ID": 371, "year": 2023, "match_id": "2023_Cádiz_Las Palmas",
     "homered1": 74},
 
    {"ID": 372, "year": 2023, "match_id": "2023_Granada_Celta Vigo",
     "homegoal1": 86, "awaygoal1": 61, "awaygoal2": 63},
 
    {"ID": 373, "year": 2023, "match_id": "2023_Mallorca_Almería",
     "homegoal1": 29, "homegoal2": 84,
     "awaygoal1": 42, "awaygoal2": 66},
 
    {"ID": 374, "year": 2023, "match_id": "2023_Valencia_Girona",
     "homegoal1": 84,
     "awaygoal1": 33, "awaygoal2": 58, "awaygoal3": 67},
 
    {"ID": 375, "year": 2023, "match_id": "2023_Villarreal_Real Madrid",
     "homegoal1": 39, "homegoal2": 48, "homegoal3": 52, "homegoal4": 56,
     "awaygoal1": 14, "awaygoal2": 30, "awaygoal3": 40, "awaygoal4": 45},
 
    {"ID": 376, "year": 2023, "match_id": "2023_Alavés_Getafe",
     "homegoal1": 12, "awayred1": 91},
 
    {"ID": 377, "year": 2023, "match_id": "2023_Real Sociedad_Valencia",
     "homegoal1": 40},
 
    {"ID": 378, "year": 2023, "match_id": "2023_Almería_Barcelona",
     "awaygoal1": 14, "awaygoal2": 67},
 
    {"ID": 379, "year": 2023, "match_id": "2023_Las Palmas_Real Betis",
     "homegoal1": 27, "homegoal2": 64,
     "awaygoal1": 21, "awaygoal2": 49},
 
    {"ID": 380, "year": 2023, "match_id": "2023_Getafe_Atlético Madrid",
     "awaygoal1": 27, "awaygoal2": 42, "awaygoal3": 51},
]
 
# ============================================================================
# LOAD AND INSERT
# ============================================================================
 
df = pd.read_excel(INPUT_FILE)
 
new_rows = []
 
for fix in MISSING_FIXES:
    row = {col: None for col in df.columns}
 
    for k, v in fix.items():
        row[k] = v
 
    # Derive Home_Team and Away_Team from match_id (format: YYYY_HomeTeam_AwayTeam)
    _, teams = fix["match_id"].split("_", 1)
    home_team, away_team = teams.split("_", 1)
    row["Home_Team"] = home_team
    row["Away_Team"] = away_team
 
    new_rows.append(row)
 
df_fixed = pd.concat([df, pd.DataFrame(new_rows)], ignore_index=True)
 
# ============================================================================
# SAVE
# ============================================================================
 
df_fixed.to_excel(OUTPUT_FILE, index=False)
 
print("Missing LaLiga 2023/24 matches inserted successfully")
print(f"   Original rows: {len(df)}")
print(f"   Rows added:    {len(new_rows)}")
print(f"   New total:     {len(df_fixed)}")
print(f"   Saved to:      {OUTPUT_FILE}")
 