# ============================================================================
# CALCULATE LIVE BETTING ODDS
# ============================================================================
# This script simulates minute-by-minute live betting odds for each match
# using Monte Carlo simulation. For each minute, it simulates 100,000
# possible match futures from that point forward, using per-minute scoring
# rates adjusted for any red cards that have occurred.
#
# Two sets of odds are produced:
#   - Standard live odds (clean_av_home/draw/away): reflect the actual
#     match state at each minute
#   - No-goal-no-red odds (clean_av_home/draw/away_nogoalnored): a
#     counterfactual set that pretends no goal or red card occurred in
#     that minute, using the previous minute's state as the baseline.
#     Useful for robustness checks and alternative analyses.
#
# A fixed random seed is set for full reproducibility.
#
# INPUT:  Minute-by-minute dataset (output of build_minute_by_minute_dataset.py)
# OUTPUT: Same dataset with six new columns of live odds appended
# ============================================================================
 
import pandas as pd
import numpy as np
import os
 
np.random.seed(482931)
 
# ============================================================================
# SETTINGS - EDIT THESE FOR YOUR LEAGUE
# ============================================================================
 
INPUT_FILE  = r"path/to/your/get_minute_betting_odds.csv"
OUTPUT_FILE = r"path/to/your/minute_betting_odds.csv"
 
os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
 
# ============================================================================
# LOAD DATA
# ============================================================================
 
dataset = pd.read_csv(INPUT_FILE)
 
# ============================================================================
# FUNCTIONS
# ============================================================================
 
def score_separator(score):
    homescore_now = []
    awayscore_now = []
    for i in score:
        home, away = map(int, i.split(','))
        homescore_now.append(home)
        awayscore_now.append(away)
    return homescore_now, awayscore_now
 
 
def all_variables(dataset):
    score = dataset['score'].dropna()
    red   = dataset['red'].dropna().tolist()
    homered,   awayred   = score_separator(red)
    homescored, awayscored = score_separator(score)
    homescoring = dataset['homescoring'].dropna().values
    awayscoring = dataset['awayscoring'].dropna().values
    home_win    = dataset['prehome'].dropna().values
    all_draw    = dataset['predraw'].dropna().values
    away_win    = dataset['preaway'].dropna().values
    return [
        homered, awayred,
        homescored, awayscored,
        homescoring, awayscoring,
        home_win, all_draw, away_win
    ]
 
 
def simulations(homered, awayred, homescoring, awayscoring):
    """
    Generates 100,000 simulated match futures for each minute.
    Red card adjustments are applied to scoring rates before simulation:
      - Team with more red cards: scoring rate * 2/3
      - Opposing team: scoring rate * 1.2
    Returns two matrices of shape (num_minutes, 100000).
    """
    homered     = np.array(homered, dtype=int)
    awayred     = np.array(awayred, dtype=int)
    homescoring = np.array(homescoring)
    awayscoring = np.array(awayscoring)
    num_minutes = len(homescoring)
 
    adjusted_homescoring = homescoring.copy()
    adjusted_awayscoring = awayscoring.copy()
 
    mask_home_more_red = homered > awayred
    adjusted_homescoring[mask_home_more_red] *= (2 / 3)
    adjusted_awayscoring[mask_home_more_red] *= 1.2
 
    mask_away_more_red = homered < awayred
    adjusted_homescoring[mask_away_more_red] *= 1.2
    adjusted_awayscoring[mask_away_more_red] *= (2 / 3)
 
    num_samples = 100000
    home_binomials = np.random.binomial(
        n=1, p=adjusted_homescoring[:, None], size=(num_minutes, num_samples)
    )
    away_binomials = np.random.binomial(
        n=1, p=adjusted_awayscoring[:, None], size=(num_minutes, num_samples)
    )
 
    return home_binomials, away_binomials
 
 
def calculate_chances(home_binomials, away_binomials, homescored, awayscored):
    """
    Calculates standard live win probabilities at each minute based on
    the actual current score and simulated remaining goals.
    """
    num_minutes, num_samples = home_binomials.shape
    homewin_chance = np.zeros(num_minutes)
    draw_chance    = np.zeros(num_minutes)
    awaywin_chance = np.zeros(num_minutes)
 
    for i in range(num_minutes):
        home_goals  = home_binomials[i:, :].sum(axis=0) + homescored[i]
        away_goals  = away_binomials[i:, :].sum(axis=0) + awayscored[i]
        differences = home_goals - away_goals
 
        home_wins = np.sum(differences > 0)
        draws     = np.sum(differences == 0)
        away_wins = np.sum(differences < 0)
        total     = home_wins + draws + away_wins
 
        homewin_chance[i] = home_wins / total
        draw_chance[i]    = draws    / total
        awaywin_chance[i] = away_wins / total
 
    return homewin_chance, draw_chance, awaywin_chance
 
 
def calculate_chances_nogoalnored(home_binomials, away_binomials,
                                   homescored, awayscored,
                                   homered, awayred):
    """
    Calculates counterfactual win probabilities at each minute as if no
    goal or red card occurred in that minute. If a goal or red card is
    detected, the previous minute's cumulative score is used as the baseline
    instead of the current minute's score. Minute 1 always uses actual state.
 
    Red card adjustments are already baked into the binomials from
    simulations() so no re-adjustment is applied here.
    """
    num_minutes, num_samples = home_binomials.shape
    homewin_chance = np.zeros(num_minutes)
    draw_chance    = np.zeros(num_minutes)
    awaywin_chance = np.zeros(num_minutes)
 
    for i in range(num_minutes):
        if i == 0:
            home_goals_now = homescored[i]
            away_goals_now = awayscored[i]
        else:
            goal_this_minute = (homescored[i] != homescored[i-1] or
                                awayscored[i] != awayscored[i-1])
            red_this_minute  = (homered[i]    != homered[i-1]    or
                                awayred[i]    != awayred[i-1])
 
            if goal_this_minute or red_this_minute:
                home_goals_now = homescored[i - 1]
                away_goals_now = awayscored[i - 1]
            else:
                home_goals_now = homescored[i]
                away_goals_now = awayscored[i]
 
        home_goals  = home_binomials[i:, :].sum(axis=0) + home_goals_now
        away_goals  = away_binomials[i:, :].sum(axis=0) + away_goals_now
        differences = home_goals - away_goals
 
        home_wins = np.sum(differences > 0)
        draws     = np.sum(differences == 0)
        away_wins = np.sum(differences < 0)
        total     = home_wins + draws + away_wins
 
        homewin_chance[i] = home_wins / total
        draw_chance[i]    = draws    / total
        awaywin_chance[i] = away_wins / total
 
    return homewin_chance, draw_chance, awaywin_chance
 
 
def game_betting_odds(game_data):
    (
        homered, awayred,
        homescored, awayscored,
        homescoring, awayscoring,
        home_win, all_draw, away_win
    ) = game_data
 
    home_binomials, away_binomials = simulations(
        homered, awayred, homescoring, awayscoring
    )
 
    homewin_chance, draw_chance, awaywin_chance = calculate_chances(
        home_binomials, away_binomials, homescored, awayscored
    )
 
    homewin_nogoalnored, draw_nogoalnored, awaywin_nogoalnored = \
        calculate_chances_nogoalnored(
            home_binomials, away_binomials,
            homescored, awayscored,
            homered, awayred
        )
 
    return (homewin_chance, draw_chance, awaywin_chance,
            homewin_nogoalnored, draw_nogoalnored, awaywin_nogoalnored)
 
 
def process_games(dataset):
    num_minutes = 92
    num_games   = len(dataset) // num_minutes
    results     = []
 
    for game_idx in range(num_games):
        start = game_idx * num_minutes
        end   = start + num_minutes
 
        game_data = [var[start:end] for var in all_variables(dataset)]
 
        (homewin_chance, draw_chance, awaywin_chance,
         homewin_nogoalnored, draw_nogoalnored,
         awaywin_nogoalnored) = game_betting_odds(game_data)
 
        game_results = pd.DataFrame({
            'homewin_chance':      homewin_chance,
            'draw_chance':         draw_chance,
            'awaywin_chance':      awaywin_chance,
            'homewin_nogoalnored': homewin_nogoalnored,
            'draw_nogoalnored':    draw_nogoalnored,
            'awaywin_nogoalnored': awaywin_nogoalnored,
        })
 
        results.append(game_results)
        print(f"Game {game_idx + 1} done")
 
    return pd.concat(results, ignore_index=True)
 
# ============================================================================
# RUN AND SAVE
# ============================================================================
 
all_results = process_games(dataset)
 
df_selected = all_results[[
    'homewin_chance', 'draw_chance', 'awaywin_chance',
    'homewin_nogoalnored', 'draw_nogoalnored', 'awaywin_nogoalnored'
]]
df_selected.columns = [
    'clean_av_home', 'clean_av_draw', 'clean_av_away',
    'clean_av_home_nogoalnored', 'clean_av_draw_nogoalnored',
    'clean_av_away_nogoalnored'
]
 
dataset = dataset.reset_index(drop=True)
dataset = pd.concat([dataset, df_selected], axis=1)
 
dataset.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")
print(f"\n Live odds file saved to:\n{OUTPUT_FILE}")