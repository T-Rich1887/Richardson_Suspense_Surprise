# ============================================================================
# CALCULATE SUSPENSE
# ============================================================================
# This script calculates the minute-by-minute suspense measure for each match.
#
# Suspense at minute t captures how much the outcome probabilities would
# change if either team scored in minute t+1, weighted by the probability
# that a goal actually occurs in that next minute. It is a forward-looking
# measure — it reflects the tension a viewer feels NOW about what might
# happen NEXT.
#
# The formula at each minute t is:
#
#   SUS_t = sqrt(
#       sum over {H,D,A}: scoring_rate_home_(t+1) * (p_if_home_goal_(t+1) - p_live_t)^2
#     + sum over {H,D,A}: scoring_rate_away_(t+1) * (p_if_away_goal_(t+1) - p_live_t)^2
#   )
#
# Where:
#   p_live_t            = current live probability of outcome k at minute t
#   p_if_home_goal_(t+1)= probability of outcome k if home team scores at t+1
#   p_if_away_goal_(t+1)= probability of outcome k if away team scores at t+1
#   scoring_rate_(t+1)  = per-minute probability of scoring at minute t+1
#
# The last minute is set to zero since there is no next minute to look forward to.
#
# A fixed random seed is set for full reproducibility.
#
# INPUT:  Live odds file (output of calculate_live_odds.py)
# OUTPUT: Same dataset with suspense and hypothetical probability columns appended
# ============================================================================
 
import pandas as pd
import numpy as np
import os
 
np.random.seed(482931)
 
# ============================================================================
# SETTINGS - EDIT THESE FOR YOUR LEAGUE
# ============================================================================
 
INPUT_FILE  = r"path/to/your/minute_betting_odds.csv"
OUTPUT_FILE = r"path/to/your/suspense_output.csv"
 
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
    homered,    awayred    = score_separator(red)
    homescored, awayscored = score_separator(score)
    homescoring = dataset['homescoring'].dropna().values
    awayscoring = dataset['awayscoring'].dropna().values
    # Use live betting odds as the baseline (not pre-match odds)
    home_win = dataset['clean_av_home'].dropna().tolist()
    all_draw = dataset['clean_av_draw'].dropna().tolist()
    away_win = dataset['clean_av_away'].dropna().tolist()
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
 
 
def calculate_chances_homescore(home_binomials, away_binomials,
                                 homescored, awayscored):
    """
    Calculates hypothetical win probabilities if the home team scores at
    each minute by adding +1 to the home team's cumulative score.
    """
    num_minutes, _ = home_binomials.shape
    homewin_chance = np.zeros(num_minutes)
    draw_chance    = np.zeros(num_minutes)
    awaywin_chance = np.zeros(num_minutes)
 
    for i in range(num_minutes):
        home_goals = home_binomials[i:, :].sum(axis=0) + homescored[i] + 1
        away_goals = away_binomials[i:, :].sum(axis=0) + awayscored[i]
        diff = home_goals - away_goals
 
        homewin_chance[i] = np.mean(diff > 0)
        draw_chance[i]    = np.mean(diff == 0)
        awaywin_chance[i] = np.mean(diff < 0)
 
    return homewin_chance, draw_chance, awaywin_chance
 
 
def calculate_chances_awayscore(home_binomials, away_binomials,
                                 homescored, awayscored):
    """
    Calculates hypothetical win probabilities if the away team scores at
    each minute by adding +1 to the away team's cumulative score.
    """
    num_minutes, _ = home_binomials.shape
    homewin_achance = np.zeros(num_minutes)
    draw_achance    = np.zeros(num_minutes)
    awaywin_achance = np.zeros(num_minutes)
 
    for i in range(num_minutes):
        home_goals = home_binomials[i:, :].sum(axis=0) + homescored[i]
        away_goals = away_binomials[i:, :].sum(axis=0) + awayscored[i] + 1
        diff = home_goals - away_goals
 
        homewin_achance[i] = np.mean(diff > 0)
        draw_achance[i]    = np.mean(diff == 0)
        awaywin_achance[i] = np.mean(diff < 0)
 
    return homewin_achance, draw_achance, awaywin_achance
 
 
def game_suspense(game_data):
    (
        homered, awayred,
        homescored, awayscored,
        homescoring, awayscoring,
        home_win, all_draw, away_win
    ) = game_data
 
    home_win    = np.array(home_win)
    all_draw    = np.array(all_draw)
    away_win    = np.array(away_win)
    homescoring = np.array(homescoring)
    awayscoring = np.array(awayscoring)
 
    home_binomials, away_binomials = simulations(
        homered, awayred, homescoring, awayscoring
    )
 
    homewin_chance, draw_chance, awaywin_chance = calculate_chances_homescore(
        home_binomials, away_binomials, homescored, awayscored
    )
 
    homewin_achance, draw_achance, awaywin_achance = calculate_chances_awayscore(
        home_binomials, away_binomials, homescored, awayscored
    )
 
    # ----------------------------------------------------------------
    # FORWARD-LOOKING SHIFT
    # Suspense at minute t uses:
    #   - current minute's live odds as the baseline (how I feel NOW)
    #   - next minute's hypothetical probs and scoring rates (what could happen NEXT)
    # All hypothetical arrays and scoring rates are rolled forward by 1.
    # The last minute is zeroed out — no next minute to look forward to.
    # ----------------------------------------------------------------
    homewin_chance_next  = np.roll(homewin_chance, -1);  homewin_chance_next[-1]  = 0
    draw_chance_next     = np.roll(draw_chance, -1);     draw_chance_next[-1]     = 0
    awaywin_chance_next  = np.roll(awaywin_chance, -1);  awaywin_chance_next[-1]  = 0
    homewin_achance_next = np.roll(homewin_achance, -1); homewin_achance_next[-1] = 0
    draw_achance_next    = np.roll(draw_achance, -1);    draw_achance_next[-1]    = 0
    awaywin_achance_next = np.roll(awaywin_achance, -1); awaywin_achance_next[-1] = 0
    homescoring_next     = np.roll(homescoring, -1);     homescoring_next[-1]     = 0
    awayscoring_next     = np.roll(awayscoring, -1);     awayscoring_next[-1]     = 0
 
    suspense = np.sqrt(
        homescoring_next * (homewin_chance_next  - home_win) ** 2 +
        homescoring_next * (draw_chance_next     - all_draw) ** 2 +
        homescoring_next * (awaywin_chance_next  - away_win) ** 2 +
        awayscoring_next * (homewin_achance_next - home_win) ** 2 +
        awayscoring_next * (draw_achance_next    - all_draw) ** 2 +
        awayscoring_next * (awaywin_achance_next - away_win) ** 2
    )
 
    return (
        suspense,
        homewin_chance, draw_chance, awaywin_chance,
        homewin_achance, draw_achance, awaywin_achance
    )
 
 
def process_games(dataset):
    num_minutes = 92
    num_games   = len(dataset) // num_minutes
    results     = []
 
    for game_idx in range(num_games):
        start = game_idx * num_minutes
        end   = start + num_minutes
 
        game_data = [var[start:end] for var in all_variables(dataset)]
 
        (
            suspense,
            homewin_chance, draw_chance, awaywin_chance,
            homewin_achance, draw_achance, awaywin_achance
        ) = game_suspense(game_data)
 
        game_results = pd.DataFrame({
            'suspense':        suspense,
            'homewin_chance':  homewin_chance,
            'draw_chance':     draw_chance,
            'awaywin_chance':  awaywin_chance,
            'homewin_achance': homewin_achance,
            'draw_achance':    draw_achance,
            'awaywin_achance': awaywin_achance,
        })
 
        results.append(game_results)
        print(f"Game {game_idx + 1} finished")
 
    return pd.concat(results, ignore_index=True)
 
# ============================================================================
# RUN AND SAVE
# ============================================================================
 
all_results = process_games(dataset)
 
dataset = dataset.reset_index(drop=True)
dataset = pd.concat([dataset, all_results], axis=1)
 
dataset.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")
print(f"\n Suspense file saved to:\n{OUTPUT_FILE}")