# ============================================================================
# CORRECT MINUTE ERRORS
# ============================================================================
# Some seasons have matches where goal or red card minutes were incorrectly
# recorded and need to be corrected to fit the 92-minute match structure:
#
#   91 -> 92 : Second-half stoppage time events that should be at minute 92
#   45 -> 46 : First-half stoppage time events that should be at minute 46
#
# Special cases are also handled where only specific columns need changing,
# or where a value must be explicitly set rather than replaced globally.
#
# Leagues covered: EPL (2010-2014), Bundesliga (2010-2014), LaLiga (2010-2014)
#
# INPUT:  Uncorrected goals/reds files (named *_bad.xlsx)
# OUTPUT: Corrected goals/reds files
# ============================================================================
 
import pandas as pd
from pathlib import Path
 
# ============================================================================
# SETTINGS - UPDATE BASE PATHS FOR YOUR SYSTEM
# ============================================================================
 
EPL_DIR = Path(r"path/to/England_Men/goals_reds_output")
BL_DIR  = Path(r"path/to/Germany_Men/goals_reds_output")
LL_DIR  = Path(r"path/to/Spain_Men/goals_reds_output")
 
# ============================================================================
# CORRECTIONS DICTIONARY
# Each season entry contains:
#   - input:   path to uncorrected file
#   - output:  path to save corrected file
#   - to_92:   match_ids where ALL minute-91 values -> 92
#   - to_46:   match_ids where ALL minute-45 values -> 46
#   - special: list of specific overrides
#       Each special entry:
#           match_id: the match to target
#           replace:  dict of {col: (from_pattern, to_val)} for regex replacements
#           set:      dict of {col: value} for hard-set values
# ============================================================================
 
CORRECTIONS = {
 
    # --------------------------------------------------------------------------
    # EPL 2013/14
    # --------------------------------------------------------------------------
    "EPL_20132014": {
        "input":  EPL_DIR / "EPL_20132014_goals_reds_bad.xlsx",
        "output": EPL_DIR / "EPL_20132014_goals_reds.xlsx",
        "to_92": [
            "2013_Crystal Palace_Sunderland",
            "2013_West Bromwich Albion_Sunderland",
            "2013_Chelsea_West Bromwich Albion",
            "2013_Norwich City_West Ham United",
            "2013_Cardiff City_Manchester United",
            "2013_Manchester City_Tottenham Hotspur",
            "2013_West Bromwich Albion_Manchester City",
            "2013_Everton_Fulham",
            "2013_Manchester City_Arsenal",
            "2013_Swansea City_Manchester City",
            "2013_Arsenal_Cardiff City",
            "2013_West Ham United_Norwich City",
            "2013_Chelsea_Everton",
            "2013_Newcastle United_Aston Villa",
            "2013_Southampton_Norwich City",
            "2013_Everton_Cardiff City",
            "2013_Newcastle United_Crystal Palace",
            "2013_Tottenham Hotspur_Southampton",
            "2013_Manchester United_Aston Villa",
            "2013_Tottenham Hotspur_Sunderland",
            "2013_Swansea City_Aston Villa",
            "2013_Newcastle United_Cardiff City",
            "2013_Manchester City_Aston Villa",
            "2013_Fulham_Crystal Palace",
            "2013_Swansea City_Manchester United",
            "2013_Cardiff City_Manchester City",
            "2013_Fulham_West Bromwich Albion",
            "2013_Cardiff City_Tottenham Hotspur",
            "2013_Fulham_Cardiff City",
            "2013_Swansea City_Stoke City",
            "2013_Cardiff City_Arsenal",
            "2013_Manchester City_Arsenal",
            "2013_Aston Villa_Crystal Palace",
            "2013_Cardiff City_Sunderland",
            "2013_Stoke City_Everton",
            "2013_Cardiff City_West Ham United",
            "2013_Newcastle United_Manchester City",
            "2013_Manchester City_Cardiff City",
            "2013_West Ham United_Newcastle United",
            "2013_Manchester United_Fulham",
            "2013_Fulham_Liverpool",
            "2013_Southampton_Liverpool",
            "2013_Hull City_Newcastle United",
            "2013_Cardiff City_Liverpool",
            "2013_Everton_Swansea City",
            "2013_West Bromwich Albion_Cardiff City",
            "2013_Newcastle United_Manchester United",
            "2013_West Bromwich Albion_Tottenham Hotspur",
            "2013_Newcastle United_Swansea City",
            "2013_Liverpool_Chelsea",
            "2013_Swansea City_Southampton",
        ],
        "to_46": [
            "2013_Everton_Chelsea",
            "2013_Manchester City_Manchester United",
            "2013_Manchester United_Crystal Palace",
            "2013_Swansea City_Newcastle United",
            "2013_Norwich City_Swansea City",
            "2013_Manchester City_Liverpool",
            "2013_Swansea City_Manchester City",
            "2013_Liverpool_Aston Villa",
            "2013_West Ham United_Newcastle United",
            "2013_West Ham United_Swansea City",
            "2013_Cardiff City_Fulham",
            "2013_Southampton_Newcastle United",
            "2013_Manchester City_Southampton",
            "2013_West Ham United_Liverpool",
            "2013_Sunderland_Cardiff City",
            "2013_Aston Villa_Hull City",
            "2013_Chelsea_Aston Villa",
            "2013_West Ham United_West Bromwich Albion",
            "2013_West Bromwich Albion_Chelsea",
            "2013_Newcastle United_Swansea City",
            "2013_Cardiff City_Stoke City",
            "2013_Liverpool_Chelsea",
            "2013_Hull City_Sunderland",
            "2013_Manchester City_Newcastle United",
        ],
        "special": [
            # awayred1 must stay 45 (override global 45->46 change)
            {
                "match_id": "2013_Sunderland_Cardiff City",
                "set": {"awayred1": 45}
            },
        ],
    },
 
    # --------------------------------------------------------------------------
    # EPL 2012/13
    # --------------------------------------------------------------------------
    "EPL_20122013": {
        "input":  EPL_DIR / "EPL_20122013_goals_reds_bad.xlsx",
        "output": EPL_DIR / "EPL_20122013_goals_reds.xlsx",
        "to_92": [
            "2012_Reading_Stoke City",
            "2012_Manchester City_Queens Park Rangers",
            "2012_Wigan Athletic_Fulham",
            "2012_West Ham United_Sunderland",
            "2012_Southampton_Aston Villa",
            "2012_Newcastle United_West Bromwich Albion",
            "2012_Newcastle United_Swansea City",
            "2012_Arsenal_Tottenham Hotspur",
            "2012_Wigan Athletic_Reading",
            "2012_West Ham United_Chelsea",
            "2012_Swansea City_Norwich City",
            "2012_Sunderland_Reading",
            "2012_Manchester City_Reading",
            "2012_Liverpool_Fulham",
            "2012_Chelsea_Aston Villa",
            "2012_Arsenal_Newcastle United",
            "2012_Swansea City_Aston Villa",
            "2012_Tottenham Hotspur_Manchester United",
            "2012_Fulham_West Ham United",
            "2012_Reading_Chelsea",
            "2012_Everton_Aston Villa",
            "2012_Newcastle United_Chelsea",
            "2012_Chelsea_Wigan Athletic",
            "2012_Norwich City_Everton",
            "2012_Manchester United_Norwich City",
            "2012_Queens Park Rangers_Sunderland",
            "2012_Newcastle United_Stoke City",
            "2012_Everton_Manchester City",
            "2012_Wigan Athletic_Newcastle United",
            "2012_Newcastle United_Fulham",
            "2012_Arsenal_Norwich City",
            "2012_Liverpool_Chelsea",
            "2012_Tottenham Hotspur_West Bromwich Albion",
            "2012_Southampton_Manchester United",
            "2012_West Bromwich Albion_Queens Park Rangers",
            "2012_West Bromwich Albion_Manchester City",
            "2012_Tottenham Hotspur_Chelsea",
            "2012_Wigan Athletic_West Ham United",
            "2012_Manchester United_Arsenal",
            "2012_Sunderland_West Bromwich Albion",
            "2012_Arsenal_Swansea City",
            "2012_Manchester City_Manchester United",
            "2012_Swansea City_Stoke City",
            "2012_Liverpool_West Bromwich Albion",
            "2012_Swansea City_Arsenal",
            "2012_Stoke City_Aston Villa",
            "2012_Queens Park Rangers_Wigan Athletic",
            "2012_Manchester City_West Ham United",
            "2012_Swansea City_Fulham",
            "2012_Aston Villa_Stoke City",
            "2012_West Ham United_Everton",
            "2012_West Ham United_West Bromwich Albion",
        ],
        "to_46": [
            "2012_Chelsea_Newcastle United",
            "2012_Swansea City_Sunderland",
            "2012_Fulham_West Bromwich Albion",
            "2012_Aston Villa_Manchester United",
            "2012_Arsenal_Tottenham Hotspur",
            "2012_Everton_West Bromwich Albion",
            "2012_Manchester United_Everton",
            "2012_Fulham_Stoke City",
            "2012_Southampton_Queens Park Rangers",
            "2012_Manchester United_Norwich City",
            "2012_Aston Villa_Queens Park Rangers",
            "2012_Manchester City_Newcastle United",
            "2012_Sunderland_Everton",
            "2012_Chelsea_Swansea City",
            "2012_Wigan Athletic_Swansea City",
            "2012_Wigan Athletic_Aston Villa",
            "2012_Swansea City_Sunderland",
            "2012_Everton_Sunderland",
            "2012_Queens Park Rangers_Southampton",
            "2012_Swansea City_West Bromwich Albion",
            "2012_Sunderland_Chelsea",
            "2012_Stoke City_Chelsea",
            "2012_Reading_Chelsea",
            "2012_Reading_Wigan Athletic",
            "2012_Stoke City_West Ham United",
            "2012_Aston Villa_Manchester City",
            "2012_Southampton_Liverpool",
        ],
        "special": [
            # homegoal1 stays 91, only homegoal2 -> 92
            {
                "match_id": "2012_Everton_Tottenham Hotspur",
                "replace": {"homegoal2": (r"\b91\b", "92")}
            },
        ],
    },
 
    # --------------------------------------------------------------------------
    # EPL 2011/12
    # --------------------------------------------------------------------------
    "EPL_20112012": {
        "input":  EPL_DIR / "EPL_20112012_goals_reds_bad.xlsx",
        "output": EPL_DIR / "EPL_20112012_goals_reds.xlsx",
        "to_92": [
            "2011_Manchester City_Swansea City",
            "2011_Chelsea_Norwich City",
            "2011_Sunderland_Chelsea",
            "2011_Everton_Wigan Athletic",
            "2011_Tottenham Hotspur_Liverpool",
            "2011_Chelsea_Swansea City",
            "2011_Manchester City_Wolverhampton Wanderers",
            "2011_Swansea City_Bolton Wanderers",
            "2011_Norwich City_Blackburn Rovers",
            "2011_Manchester City_Norwich City",
            "2011_Swansea City_Fulham",
            "2011_Sunderland_Blackburn Rovers",
            "2011_Norwich City_Fulham",
            "2011_Sunderland_Manchester City",
            "2011_Fulham_Arsenal",
            "2011_Manchester City_Tottenham Hotspur",
            "2011_Arsenal_Blackburn Rovers",
            "2011_West Bromwich Albion_Sunderland",
            "2011_Newcastle United_Sunderland",
            "2011_Aston Villa_Fulham",
            "2011_Arsenal_Newcastle United",
            "2011_Liverpool_Everton",
            "2011_Tottenham Hotspur_Stoke City",
            "2011_Queens Park Rangers_Liverpool",
            "2011_Arsenal_Aston Villa",
            "2011_Wigan Athletic_Stoke City",
            "2011_Chelsea_Wigan Athletic",
            "2011_Manchester United_Aston Villa",
            "2011_Manchester City_Queens Park Rangers",
            "2011_Norwich City_Stoke City",
            "2011_Liverpool_Bolton Wanderers",
            "2011_Blackburn Rovers_Everton",
            "2011_Tottenham Hotspur_Manchester City",
            "2011_Wigan Athletic_Bolton Wanderers",
            "2011_Bolton Wanderers_Sunderland",
            "2011_Manchester United_Manchester City",
            "2011_Chelsea_Arsenal",
            "2011_Fulham_Tottenham Hotspur",
            "2011_Wigan Athletic_Blackburn Rovers",
            "2011_West Bromwich Albion_Tottenham Hotspur",
            "2011_Sunderland_Wigan Athletic",
            "2011_Newcastle United_Chelsea",
            "2011_Stoke City_West Bromwich Albion",
            "2011_Swansea City_Chelsea",
            "2011_Blackburn Rovers_Newcastle United",
            "2011_Sunderland_Arsenal",
            "2011_Blackburn Rovers_Queens Park Rangers",
            "2011_Norwich City_Manchester United",
            "2011_Liverpool_Arsenal",
            "2011_Aston Villa_Chelsea",
            "2011_Blackburn Rovers_Liverpool",
            "2011_Norwich City_Manchester City",
            "2011_Chelsea_Newcastle United",
            "2011_Queens Park Rangers_Bolton Wanderers",
            "2011_Aston Villa_Arsenal",
            "2011_Aston Villa_Sunderland",
        ],
        "to_46": [
            "2011_Wolverhampton Wanderers_Fulham",
            "2011_Chelsea_Everton",
            "2011_Liverpool_Norwich City",
            "2011_Manchester United_Sunderland",
            "2011_Blackburn Rovers_Swansea City",
            "2011_Manchester United_Bolton Wanderers",
            "2011_Blackburn Rovers_Fulham",
            "2011_Blackburn Rovers_Queens Park Rangers",
            "2011_Wolverhampton Wanderers_West Bromwich Albion",
            "2011_Norwich City_Wolverhampton Wanderers",
            "2011_Queens Park Rangers_Swansea City",
            "2011_Wigan Athletic_Newcastle United",
            "2011_Manchester City_Manchester United",
            "2011_Queens Park Rangers_Bolton Wanderers",
            "2011_Manchester United_Arsenal",
            "2011_Wigan Athletic_Bolton Wanderers",
            "2011_West Bromwich Albion_Liverpool",
            "2011_Norwich City_Blackburn Rovers",
            "2011_Newcastle United_Everton",
            "2011_Fulham_Tottenham Hotspur",
            "2011_Norwich City_Newcastle United",
            "2011_Wigan Athletic_Sunderland",
            "2011_Newcastle United_Aston Villa",
            "2011_Wigan Athletic_Swansea City",
            "2011_Wolverhampton Wanderers_Manchester United",
            "2011_Manchester City_Sunderland",
            "2011_Bolton Wanderers_Norwich City",
        ],
        "special": [
            # homegoal1 -> 92, homered1 stays 91
            {
                "match_id": "2011_Queens Park Rangers_Aston Villa",
                "replace": {"homegoal1": (r"\b91\b", "92")}
            },
            # awaygoal3 -> 92, homegoal2 stays 91
            {
                "match_id": "2011_Fulham_Everton",
                "replace": {"awaygoal3": (r"\b91\b", "92")}
            },
        ],
    },
 
    # --------------------------------------------------------------------------
    # EPL 2010/11
    # --------------------------------------------------------------------------
    "EPL_20102011": {
        "input":  EPL_DIR / "EPL_20102011_goals_reds_bad.xlsx",
        "output": EPL_DIR / "EPL_20102011_goals_reds.xlsx",
        "to_92": [
            "2010_Newcastle United_Aston Villa",
            "2010_Sunderland_Manchester City",
            "2010_Everton_Manchester United",
            "2010_Fulham_Wolverhampton Wanderers",
            "2010_Stoke City_Aston Villa",
            "2010_Sunderland_Arsenal",
            "2010_Tottenham Hotspur_Wolverhampton Wanderers",
            "2010_Arsenal_West Bromwich Albion",
            "2010_Newcastle United_Wigan Athletic",
            "2010_Bolton Wanderers_Stoke City",
            "2010_Manchester United_Wolverhampton Wanderers",
            "2010_Bolton Wanderers_Tottenham Hotspur",
            "2010_Fulham_Aston Villa",
            "2010_Everton_Bolton Wanderers",
            "2010_Stoke City_Liverpool",
            "2010_Bolton Wanderers_Newcastle United",
            "2010_Stoke City_Manchester City",
            "2010_Tottenham Hotspur_Liverpool",
            "2010_Newcastle United_Liverpool",
            "2010_Liverpool_Bolton Wanderers",
            "2010_Sunderland_Newcastle United",
            "2010_Everton_West Ham United",
            "2010_Bolton Wanderers_Wolverhampton Wanderers",
            "2010_Stoke City_Sunderland",
            "2010_Tottenham Hotspur_Bolton Wanderers",
            "2010_Birmingham City_Stoke City",
            "2010_West Bromwich Albion_Wolverhampton Wanderers",
            "2010_West Ham United_Liverpool",
            "2010_Blackburn Rovers_Blackpool",
            "2010_Wigan Athletic_Birmingham City",
            "2010_Stoke City_Newcastle United",
            "2010_Chelsea_Manchester City",
            "2010_Newcastle United_Wolverhampton Wanderers",
            "2010_Arsenal_Liverpool",
            "2010_Chelsea_West Ham United",
            "2010_Wigan Athletic_West Ham United",
            "2010_Tottenham Hotspur_Birmingham City",
            "2010_Blackpool_Blackburn Rovers",
            "2010_Birmingham City_Everton",
            "2010_Newcastle United_Sunderland",
            "2010_Wolverhampton Wanderers_Arsenal",
            "2010_West Bromwich Albion_Stoke City",
            "2010_Aston Villa_Arsenal",
            "2010_West Bromwich Albion_Newcastle United",
            "2010_Blackburn Rovers_Stoke City",
            "2010_Chelsea_Aston Villa",
            "2010_Newcastle United_Tottenham Hotspur",
            "2010_Wolverhampton Wanderers_Liverpool",
            "2010_Sunderland_Chelsea",
            "2010_Blackpool_Tottenham Hotspur",
            "2010_Liverpool_Manchester United",
            "2010_West Ham United_Aston Villa",
            "2010_Arsenal_Liverpool",
            "2010_Bolton Wanderers_Sunderland",
            "2010_Chelsea_Newcastle United",
            "2010_West Ham United_Sunderland",
            "2010_Arsenal_Birmingham City",
            "2010_Arsenal_Newcastle United",
            "2010_Chelsea_Fulham",
            "2010_Manchester City_Everton",
            "2010_Aston Villa_Blackburn Rovers",
            "2010_Chelsea_Manchester United",
        ],
        "to_46": [
            "2010_Tottenham Hotspur_Aston Villa",
            "2010_Newcastle United_Sunderland",
            "2010_Blackburn Rovers_Aston Villa",
            "2010_Fulham_West Bromwich Albion",
            "2010_Manchester United_Birmingham City",
            "2010_Manchester United_Aston Villa",
            "2010_Bolton Wanderers_Aston Villa",
            "2010_Blackburn Rovers_Birmingham City",
            "2010_Stoke City_Wolverhampton Wanderers",
            "2010_Liverpool_Blackpool",
            "2010_Aston Villa_Blackpool",
            "2010_Fulham_West Ham United",
            "2010_Fulham_Blackburn Rovers",
            "2010_Blackpool_Wigan Athletic",
            "2010_Bolton Wanderers_Sunderland",
            "2010_Wolverhampton Wanderers_Blackburn Rovers",
            "2010_Liverpool_Arsenal",
            "2010_Blackburn Rovers_Sunderland",
        ],
        "special": [
            # awaygoal3 stays 91, homegoal2 -> 92
            {
                "match_id": "2010_Blackpool_Manchester City",
                "replace": {"homegoal2": (r"\b91\b", "92")}
            },
            # awaygoal1 stays 91, awayred1 -> 92
            {
                "match_id": "2010_Liverpool_Arsenal",
                "replace": {"awayred1": (r"\b91\b", "92")}
            },
            # homegoal5 stays 91, awaygoal6 -> 92
            {
                "match_id": "2010_Wigan Athletic_Chelsea",
                "replace": {"awaygoal6": (r"\b91\b", "92")}
            },
        ],
    },
 
    # --------------------------------------------------------------------------
    # BUNDESLIGA 2013/14
    # --------------------------------------------------------------------------
    "Bundesliga_20132014": {
        "input":  BL_DIR / "Bundesliga_20132014_goals_reds_bad.xlsx",
        "output": BL_DIR / "Bundesliga_20132014_goals_reds.xlsx",
        "to_92": [
            "2013_Wolfsburg_Schalke 04",
            "2013_Hamburger SV_Eintracht Braunschweig",
            "2013_Bayer Leverkusen_Wolfsburg",
            "2013_Mainz 05_Hoffenheim",
            "2013_Bayern Munich_Augsburg",
            "2013_Schalke 04_Werder Bremen",
            "2013_Bayern Munich_Hamburger SV",
            "2013_Hannover 96_NÃ¼rnberg",
            "2013_Mainz 05_Hannover 96",
            "2013_Hoffenheim_Stuttgart",
            "2013_Eintracht Braunschweig_Hamburger SV",
            "2013_Hamburger SV_Dortmund",
            "2013_Schalke 04_Eintracht Braunschweig",
            "2013_Hoffenheim_Hannover 96",
            "2013_Schalke 04_Eintracht Frankfurt",
            "2013_Werder Bremen_Hoffenheim",
            "2013_Werder Bremen_Hertha BSC",
            "2013_Bayern Munich_Stuttgart",
            "2013_Schalke 04_NÃ¼rnberg",
            "2013_Hamburger SV_Werder Bremen",
            "2013_Eintracht Braunschweig_Schalke 04",
            "2013_Hertha BSC_Schalke 04",
            "2013_Hoffenheim_Werder Bremen",
            "2013_Mainz 05_Dortmund",
            "2013_Freiburg_Wolfsburg",
            "2013_Freiburg_Hannover 96",
            "2013_Hamburger SV_Mainz 05",
            "2013_Stuttgart_Bayern Munich",
            "2013_Hertha BSC_NÃ¼rnberg",
            "2013_Freiburg_Augsburg",
            "2013_Hoffenheim_Mainz 05",
            "2013_Bayern Munich_Bayer Leverkusen",
            "2013_Hertha BSC_Hannover 96",
            "2013_Eintracht Frankfurt_Freiburg",
            "2013_Hamburger SV_NÃ¼rnberg",
            "2013_Hannover 96_Dortmund",
            "2013_NÃ¼rnberg_Eintracht Frankfurt",
            "2013_Stuttgart_Wolfsburg",
            "2013_Eintracht Braunschweig_Augsburg",
            "2013_Dortmund_Bayer Leverkusen",
            "2013_Wolfsburg_Augsburg",
            "2013_Bayern Munich_Dortmund",
            "2013_Hertha BSC_MÃ¶nchengladbach",
            "2013_Eintracht Braunschweig_Bayer Leverkusen",
            "2013_NÃ¼rnberg_Mainz 05",
            "2013_Stuttgart_Hertha BSC",
            "2013_Freiburg_NÃ¼rnberg",
        ],
        "to_46": [
            "2013_Schalke 04_Hamburger SV",
            "2013_Wolfsburg_Hertha BSC",
            "2013_Dortmund_Freiburg",
            "2013_MÃ¶nchengladbach_Schalke 04",
            "2013_Eintracht Braunschweig_Mainz 05",
            "2013_Eintracht Frankfurt_Hamburger SV",
            "2013_Wolfsburg_Dortmund",
            "2013_Hoffenheim_Werder Bremen",
            "2013_Augsburg_Werder Bremen",
        ],
        "special": [
            # awaygoal1 and awaygoal2 hard-set to specific values
            {
                "match_id": "2013_Hoffenheim_Werder Bremen",
                "set": {"awaygoal1": 45, "awaygoal2": 46}
            },
        ],
    },
 
    # --------------------------------------------------------------------------
    # BUNDESLIGA 2012/13
    # --------------------------------------------------------------------------
    "Bundesliga_20122013": {
        "input":  BL_DIR / "Bundesliga_20122013_goals_reds_bad.xlsx",
        "output": BL_DIR / "Bundesliga_20122013_goals_reds.xlsx",
        "to_92": [
            "2012_Hannover 96_Werder Bremen",
            "2012_Bayern Munich_Mainz 05",
            "2012_Hoffenheim_Hannover 96",
            "2012_MÃ¶nchengladbach_Hamburger SV",
            "2012_Freiburg_NÃ¼rnberg",
            "2012_Hoffenheim_Schalke 04",
            "2012_Hamburger SV_Schalke 04",
            "2012_NÃ¼rnberg_DÃ¼sseldorf",
            "2012_Mainz 05_Stuttgart",
            "2012_DÃ¼sseldorf_Augsburg",
            "2012_NÃ¼rnberg_Hannover 96",
            "2012_Freiburg_MÃ¶nchengladbach",
            "2012_Hoffenheim_DÃ¼sseldorf",
            "2012_Dortmund_Augsburg",
            "2012_Schalke 04_Stuttgart",
            "2012_Mainz 05_MÃ¶nchengladbach",
            "2012_Hoffenheim_Greuther FÃ¼rth",
            "2012_Greuther FÃ¼rth_MÃ¶nchengladbach",
            "2012_Wolfsburg_Bayer Leverkusen",
            "2012_Schalke 04_Hannover 96",
            "2012_Schalke 04_Greuther FÃ¼rth",
            "2012_Stuttgart_Werder Bremen",
            "2012_Wolfsburg_Bayern Munich",
            "2012_Augsburg_Hoffenheim",
            "2012_Freiburg_Wolfsburg",
            "2012_Augsburg_Hannover 96",
            "2012_Werder Bremen_Hoffenheim",
            "2012_Eintracht Frankfurt_Freiburg",
            "2012_Hamburger SV_Werder Bremen",
        ],
        "to_46": [
            "2012_DÃ¼sseldorf_Hamburger SV",
            "2012_Dortmund_Freiburg",
            "2012_Eintracht Frankfurt_Hamburger SV",
            "2012_Augsburg_Mainz 05",
        ],
        "special": [],
    },
 
    # --------------------------------------------------------------------------
    # BUNDESLIGA 2011/12
    # --------------------------------------------------------------------------
    "Bundesliga_20112012": {
        "input":  BL_DIR / "Bundesliga_20112012_goals_reds_bad.xlsx",
        "output": BL_DIR / "Bundesliga_20112012_goals_reds.xlsx",
        "to_92": [
            "2011_Freiburg_Mainz 05",
            "2011_Werder Bremen_Freiburg",
            "2011_Werder Bremen_Hertha BSC",
            "2011_Freiburg_Hertha BSC",
            "2011_Augsburg_Wolfsburg",
            "2011_Bayern Munich_Wolfsburg",
            "2011_Augsburg_Hertha BSC",
            "2011_Dortmund_Hannover 96",
            "2011_Bayern Munich_Stuttgart",
            "2011_Freiburg_KÃ¶ln",
            "2011_Hertha BSC_Hoffenheim",
            "2011_KÃ¶ln_Wolfsburg",
            "2011_Wolfsburg_Bayern Munich",
            "2011_Mainz 05_Schalke 04",
            "2011_Bayer Leverkusen_KÃ¶ln",
            "2011_Mainz 05_Dortmund",
            "2011_NÃ¼rnberg_Freiburg",
            "2011_Hoffenheim_Freiburg",
            "2011_Hoffenheim_Hertha BSC",
            "2011_Hamburger SV_Stuttgart",
            "2011_Wolfsburg_Bayer Leverkusen",
            "2011_Werder Bremen_Augsburg",
            "2011_Dortmund_Stuttgart",
            "2011_Hannover 96_Dortmund",
            "2011_Mainz 05_Stuttgart",
            "2011_Augsburg_Bayern Munich",
            "2011_NÃ¼rnberg_Hoffenheim",
            "2011_Bayer Leverkusen_Stuttgart",
        ],
        "to_46": [
            "2011_Stuttgart_Werder Bremen",
            "2011_Mainz 05_Hoffenheim",
            "2011_Hannover 96_Werder Bremen",
            "2011_Stuttgart_Dortmund",
            "2011_Freiburg_Hertha BSC",
            "2011_Hertha BSC_Hamburger SV",
            "2011_Freiburg_NÃ¼rnberg",
            "2011_Wolfsburg_Werder Bremen",
        ],
        "special": [],
    },
 
    # --------------------------------------------------------------------------
    # BUNDESLIGA 2010/11
    # --------------------------------------------------------------------------
    "Bundesliga_20102011": {
        "input":  BL_DIR / "Bundesliga_20102011_goals_reds_bad.xlsx",
        "output": BL_DIR / "Bundesliga_20102011_goals_reds.xlsx",
        "to_92": [
            "2010_Bayern Munich_Wolfsburg",
            "2010_Werder Bremen_KÃ¶ln",
            "2010_Hoffenheim_Schalke 04",
            "2010_Hannover 96_Werder Bremen",
            "2010_Mainz 05_KÃ¶ln",
            "2010_Bayer Leverkusen_Eintracht Frankfurt",
            "2010_NÃ¼rnberg_Stuttgart",
            "2010_Bayern Munich_Hannover 96",
            "2010_Dortmund_Hoffenheim",
            "2010_Werder Bremen_NÃ¼rnberg",
            "2010_NÃ¼rnberg_KÃ¶ln",
            "2010_Hannover 96_Hamburger SV",
            "2010_Hoffenheim_Bayer Leverkusen",
            "2010_Wolfsburg_Hoffenheim",
            "2010_Werder Bremen_Hoffenheim",
            "2010_Bayern Munich_Kaiserslautern",
            "2010_Hoffenheim_St. Pauli",
            "2010_Kaiserslautern_Dortmund",
            "2010_NÃ¼rnberg_Eintracht Frankfurt",
            "2010_Bayer Leverkusen_Stuttgart",
            "2010_Werder Bremen_Bayer Leverkusen",
            "2010_Kaiserslautern_Freiburg",
            "2010_Stuttgart_Wolfsburg",
            "2010_KÃ¶ln_NÃ¼rnberg",
            "2010_Freiburg_St. Pauli",
            "2010_Werder Bremen_KÃ¶ln",
            "2010_Hannover 96_Bayer Leverkusen",
            "2010_Hoffenheim_Bayern Munich",
            "2010_KÃ¶ln_Dortmund",
            "2010_Hoffenheim_MÃ¶nchengladbach",
            "2010_St. Pauli_Eintracht Frankfurt",
            "2010_Hannover 96_Dortmund",
            "2010_KÃ¶ln_MÃ¶nchengladbach",
            "2010_Hoffenheim_Freiburg",
            "2010_Eintracht Frankfurt_Hoffenheim",
            "2010_Mainz 05_Werder Bremen",
            "2010_Freiburg_Werder Bremen",
            "2010_Werder Bremen_MÃ¶nchengladbach",
            "2010_Wolfsburg_NÃ¼rnberg",
            "2010_Hamburger SV_Dortmund",
            "2010_Kaiserslautern_NÃ¼rnberg",
            "2010_Eintracht Frankfurt_KÃ¶ln",
            "2010_Kaiserslautern_Bayern Munich",
            "2010_MÃ¶nchengladbach_St. Pauli",
            "2010_Freiburg_Schalke 04",
            "2010_NÃ¼rnberg_Bayern Munich",
        ],
        "to_46": [
            "2010_St. Pauli_NÃ¼rnberg",
            "2010_Bayer Leverkusen_Bayern Munich",
            "2010_Schalke 04_Werder Bremen",
            "2010_Dortmund_MÃ¶nchengladbach",
            "2010_Bayern Munich_Kaiserslautern",
            "2010_Stuttgart_NÃ¼rnberg",
            "2010_Wolfsburg_MÃ¶nchengladbach",
            "2010_Bayer Leverkusen_Wolfsburg",
            "2010_Schalke 04_Eintracht Frankfurt",
            "2010_Hannover 96_Mainz 05",
            "2010_Bayern Munich_Bayer Leverkusen",
            "2010_Wolfsburg_NÃ¼rnberg",
        ],
        "special": [
            # homegoal1 hard-set to 46, awayred1 must stay 45
            {
                "match_id": "2010_Hannover 96_Mainz 05",
                "set": {"homegoal1": 46, "awayred1": 45}
            },
        ],
    },
 
    # --------------------------------------------------------------------------
    # LALIGA 2013/14
    # --------------------------------------------------------------------------
    "LaLiga_20132014": {
        "input":  LL_DIR / "LaLiga_20132014_goals_reds_bad.xlsx",
        "output": LL_DIR / "LaLiga_20132014_goals_reds.xlsx",
        "to_92": [],
        "to_46": ["2013_Valencia_Barcelona"],
        "special": [],
    },
 
    # --------------------------------------------------------------------------
    # LALIGA 2012/13
    # --------------------------------------------------------------------------
    "LaLiga_20122013": {
        "input":  LL_DIR / "LaLiga_20122013_goals_reds_bad.xlsx",
        "output": LL_DIR / "LaLiga_20122013_goals_reds.xlsx",
        "to_92": [],
        "to_46": [
            "2012_Athletic Club_Sevilla",
            "2012_Espanyol_Valencia",
            "2012_Real Madrid_MÃ¡laga",
        ],
        "special": [],
    },
 
    # --------------------------------------------------------------------------
    # LALIGA 2011/12
    # --------------------------------------------------------------------------
    "LaLiga_20112012": {
        "input":  LL_DIR / "LaLiga_20112012_goals_reds_bad.xlsx",
        "output": LL_DIR / "LaLiga_20112012_goals_reds.xlsx",
        "to_92": [],
        "to_46": [
            "2011_Athletic Club_Osasuna",
            "2011_Sporting GijÃ³n_Getafe",
            "2011_Rayo Vallecano_Sevilla",
            "2011_Real Madrid_Racing Santander",
            "2011_MÃ¡laga_Zaragoza",
            "2011_Mallorca_Osasuna",
            "2011_Sporting GijÃ³n_Real Betis",
            "2011_Valencia_Osasuna",
        ],
        "special": [],
    },
 
    # --------------------------------------------------------------------------
    # LALIGA 2010/11
    # --------------------------------------------------------------------------
    "LaLiga_20102011": {
        "input":  LL_DIR / "LaLiga_20102011_goals_reds_bad.xlsx",
        "output": LL_DIR / "LaLiga_20102011_goals_reds.xlsx",
        "to_92": [],
        "to_46": [
            "2010_AtlÃ©tico Madrid_Espanyol",
            "2010_MÃ¡laga_Sevilla",
            "2010_Sporting GijÃ³n_Real Sociedad",
            "2010_Real Sociedad_Valencia",
            "2010_Valencia_Espanyol",
            "2010_Athletic Club_Deportivo La CoruÃ±a",
        ],
        "special": [],
    },
}
 
# ============================================================================
# CORRECTION FUNCTION
# ============================================================================
 
def apply_corrections(season_key, config):
 
    print(f"\nProcessing: {season_key}")
 
    df = pd.read_excel(config["input"])
 
    minute_cols = [
        c for c in df.columns
        if any(k in c.lower() for k in ["goal", "red"])
    ]
 
    mask_all_edited = pd.Series(False, index=df.index)
 
    # --- 91 -> 92 global corrections ---
    if config["to_92"]:
        mask = df["match_id"].isin(config["to_92"])
        for col in minute_cols:
            df.loc[mask, col] = (
                df.loc[mask, col]
                .astype(str)
                .str.replace(r"\b91\b", "92", regex=True)
            )
        mask_all_edited = mask_all_edited | mask
 
    # --- 45 -> 46 global corrections ---
    if config["to_46"]:
        mask = df["match_id"].isin(config["to_46"])
        for col in minute_cols:
            df.loc[mask, col] = (
                df.loc[mask, col]
                .astype(str)
                .str.replace(r"\b45\b", "46", regex=True)
            )
        mask_all_edited = mask_all_edited | mask
 
    # --- Special case corrections ---
    for special in config["special"]:
        mask = df["match_id"] == special["match_id"]
 
        # Regex replacements for specific columns
        if "replace" in special:
            for col, (pattern, replacement) in special["replace"].items():
                df.loc[mask, col] = (
                    df.loc[mask, col]
                    .astype(str)
                    .str.replace(pattern, replacement, regex=True)
                )
 
        # Hard-set values for specific columns
        if "set" in special:
            for col, value in special["set"].items():
                df.loc[mask, col] = value
 
        mask_all_edited = mask_all_edited | mask
 
    # --- Convert all edited rows back to numeric ---
    for col in minute_cols:
        df.loc[mask_all_edited, col] = (
            pd.to_numeric(df.loc[mask_all_edited, col], errors="coerce")
            .astype("Int64")
        )
 
    df.to_excel(config["output"], index=False)
 
    print(f"  Matches edited: {mask_all_edited.sum()}")
    print(f"  Saved to: {config['output']}")
 
 
# ============================================================================
# RUN ALL CORRECTIONS
# ============================================================================
 
for season_key, config in CORRECTIONS.items():
    apply_corrections(season_key, config)
 
print("\nAll corrections complete!")
 