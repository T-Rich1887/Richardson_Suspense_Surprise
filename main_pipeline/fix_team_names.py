# ============================================================================
# FIX TEAM NAMES
# ============================================================================
# This script fixes broken team name encodings and normalizes team names
# across seasons in the combined goals/reds files. Broken encodings occur
# when special characters (accented letters etc.) are read incorrectly
# from the raw data source.
#
# This script is specific to the data source used in this project.
# Users replicating with a different data source should verify their own
# team names match across files and adjust the mappings below accordingly.
#
# Leagues covered: Ligue 1 (France), Bundesliga (Germany), La Liga (Spain)
#
# INPUT:  Combined all-seasons goals/reds file (one per league)
# OUTPUT: Corrected CSV file with fixed team names and rebuilt match_ids
# ============================================================================
 
import pandas as pd
from pathlib import Path
 
# ============================================================================
# SETTINGS - UPDATE BASE PATHS FOR YOUR SYSTEM
# ============================================================================
 
FRANCE_DIR  = Path(r"path/to/France_Men/goals_reds_output")
GERMANY_DIR = Path(r"path/to/Germany_Men/goals_reds_output")
SPAIN_DIR   = Path(r"path/to/Spain_Men/goals_reds_output")
 
# ============================================================================
# LEAGUE CONFIGURATIONS
# Each league entry contains:
#   - input:   combined all-seasons goals/reds file
#   - output:  corrected output file
#   - fixes:   dict of {broken_name: correct_name}
# ============================================================================
 
LEAGUES = {
 
    # --------------------------------------------------------------------------
    # LIGUE 1 (FRANCE)
    # --------------------------------------------------------------------------
    "Ligue1": {
        "input":  FRANCE_DIR / "Ligue1_allseasons_goals_reds.csv",
        "output": FRANCE_DIR / "Ligue1_allseasons_goals_reds_FIXEDNAMES.csv",
        "fixes": {
            "NÃ®mes":            "Nîmes",
            "Saint-Ã‰tienne":    "Saint-Étienne",
            "GazÃ©lec Ajaccio":  "Gazélec Ajaccio",
            "Evian":             "Évian",
        },
    },
 
    # --------------------------------------------------------------------------
    # BUNDESLIGA (GERMANY)
    # --------------------------------------------------------------------------
    "Bundesliga": {
        "input":  GERMANY_DIR / "Bundesliga_allseasons_goals_reds.csv",
        "output": GERMANY_DIR / "Bundesliga_allseasons_goals_reds_FIXEDNAMES.csv",
        "fixes": {
            "KÃ¶ln":            "Köln",
            "MÃ¶nchengladbach": "Mönchengladbach",
            "NÃ¼rnberg":        "Nürnberg",
            "DÃ¼sseldorf":      "Düsseldorf",
            "Greuther FÃ¼rth":  "Greuther Fürth",
        },
    },
 
    # --------------------------------------------------------------------------
    # LA LIGA (SPAIN)
    # Includes both encoding fixes and canonical name normalization
    # (some clubs appear under different names across seasons)
    # --------------------------------------------------------------------------
    "LaLiga": {
        "input":  SPAIN_DIR / "LaLiga_allseasons_goals_reds.csv",
        "output": SPAIN_DIR / "LaLiga_allseasons_goals_reds_FIXEDNAMES.csv",
        "fixes": {
            # Encoding fixes
            "AlavÃ©s":                "Alavés",
            "AlmerÃ\xada":            "Almería",
            "AtlÃ©tico Madrid":       "Atlético Madrid",
            "CÃ¡diz":                 "Cádiz",
            "CÃ³rdoba":               "Córdoba",
            "Deportivo La CoruÃ±a":   "Deportivo La Coruña",
            "HÃ©rcules":              "Hércules",
            "LeganÃ©s":               "Leganés",
            "MÃ¡laga":                "Málaga",
            "Sporting GijÃ³n":        "Sporting Gijón",
            # Canonical name normalization
            "Cádiz CF":               "Cádiz",
            "Granada CF":             "Granada",
            "UD Almería":             "Almería",
            "RCD Mallorca":           "Mallorca",
            "RC Celta":               "Celta Vigo",
            "Real Betis Balompié":    "Real Betis",
            "Athletic Bilbao":        "Athletic Club",
            "Ath. Bilbao":            "Athletic Club",
            "Atlético de Madrid":     "Atlético Madrid",
        },
    },
}
 
# ============================================================================
# APPLY FIXES
# ============================================================================
 
def fix_team_names(league_key, config):
 
    print(f"\nProcessing: {league_key}")
 
    df = pd.read_csv(config["input"])
 
    df["Home_Team"] = df["Home_Team"].replace(config["fixes"])
    df["Away_Team"] = df["Away_Team"].replace(config["fixes"])
 
    # Rebuild match_id using corrected names
    df["match_id"] = (
        df["year"].astype(str) + "_" +
        df["Home_Team"] + "_" +
        df["Away_Team"]
    )
 
    df.to_csv(config["output"], index=False)
 
    print(f"  Unique home teams: {df['Home_Team'].nunique()}")
    print(f"  Unique away teams: {df['Away_Team'].nunique()}")
    print(f"  Saved to: {config['output']}")
 
 
for league_key, config in LEAGUES.items():
    fix_team_names(league_key, config)
 
print("\n All team name fixes complete!")