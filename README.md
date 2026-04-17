# Replication Package: Calculating Suspense, Surprise, and Shock in Soccer Matches

This repository contains the full replication package for the paper:

> **[Paper Title]**
> [Author Names]
> [Journal Name], [Year]

All scripts are written in Python and results are fully reproducible via a fixed random seed (482931). A detailed description of the methodology is provided in `documentation/suspense_documentation.pdf`.

---

## Repository Structure

```
repository/
│
├── README.md
│
├── main_pipeline/
│   ├── clean_bookmaker_odds.py
│   ├── fit_scoring_rates.py
│   ├── extract_goals_reds.py
│   ├── combine_season_files.py
│   ├── build_empirical_distributions.py
│   ├── fix_team_names.py
│   ├── build_minutebyminute_dataset.py
│   ├── calculate_live_odds.py
│   ├── calculate_suspense.py
│   ├── calculate_surprise_shock.py
│   ├── calculate_league_averages.py
│   ├── calculate_team_averages.py
│   ├── build_plotting_file.py
│   ├── plot_league_figures.py
│   └── calculate_descriptives.py
│
├── data_corrections/
│   ├── correct_minute_errors.py
│   ├── insert_missing_matches.py
│   ├── fix_specific_match_errors.py
│   └── DATA_CORRECTIONS_NOTES.md
│
└── documentation/
    └── suspense_documentation.pdf
```

---

## Requirements

The following Python libraries are required:

```
pandas
numpy
scipy
matplotlib
pathlib
collections
re
glob
```

Install all dependencies with:

```bash
pip install pandas numpy scipy matplotlib
```

---

## Using These Measures With Your Own Data

If you are applying the suspense, surprise, and shock measures to your own data rather than replicating our exact results, you only need the following scripts in order:

1. `clean_bookmaker_odds.py` — Remove bookmaker overround from raw odds
2. `fit_scoring_rates.py` — Fit per-match Poisson scoring rates to cleaned odds
3. `extract_goals_reds.py` — Extract goal and red card minutes from raw event data
4. `combine_season_files.py` — Combine individual season files into one
5. `build_empirical_distributions.py` — Build minute-by-minute goal and red card distributions
6. `build_minutebyminute_dataset.py` — Merge all inputs into a minute-by-minute dataset
7. `calculate_live_odds.py` — Simulate live betting odds using 100,000 Monte Carlo draws per game-minute
8. `calculate_suspense.py` — Calculate the suspense measure
9. `calculate_surprise_shock.py` — Calculate the surprise measure

The remaining scripts (10-15) reproduce the specific results, figures, and descriptive statistics from our paper and are not required for applying the measures to new data.

**Important notes for new data:**
- Update all file paths in the `SETTINGS` section at the top of each script
- In `build_minutebyminute_dataset.py`, verify that team names match between your bookmaker odds file and your match event file. The `TEAM_NAME_MAPPING` dictionary maps abbreviated names from the odds source to full names from the event source — adjust this for your data source
- In `fix_team_names.py`, update or replace the encoding fixes and canonical name mappings to match your data
- The data corrections scripts are specific to our raw data source and are not needed for new data

---

## Full Replication With Our Exact Data

To exactly replicate our results using the same raw data source, run all scripts in the following order. Before running, update all file paths in the `SETTINGS` section at the top of each script to match your local directory structure.

### Step 1: Data Corrections

These scripts fix specific errors in the raw data. Run these before any other scripts. See `data_corrections/DATA_CORRECTIONS_NOTES.md` for a full explanation of each correction.

1. `data_corrections/correct_minute_errors.py` — Fixes incorrectly recorded stoppage time minutes (91→92 and 45→46) for specific matches in EPL seasons 2010-2014, Bundesliga seasons 2010-2014, and La Liga seasons 2010-2014
2. `data_corrections/insert_missing_matches.py` — Inserts 18 matches missing from the La Liga 2023/24 raw data file
3. `data_corrections/fix_specific_match_errors.py` — Fixes a wrong season year for one Bundesliga match and removes an incorrectly included playoff game from Serie A

### Step 2: Main Pipeline

Run these scripts in order after all data corrections have been applied.

**1. `clean_bookmaker_odds.py`**
Converts raw bookmaker odds to true implied probabilities by removing the overround. Processes both match result odds (home/draw/away) and over/under goal line odds (0.5 through 5.5).
- Input: Raw bookmaker odds Excel file (one row per match, from data source)
- Output: Cleaned odds CSV file with implied probabilities appended

**2. `fit_scoring_rates.py`**
Fits Poisson-based scoring rates to the cleaned bookmaker odds for each match using a grid search over 3,600 lambda pairs. Selects the home and away scoring rate combination that minimizes the sum of squared errors between model predictions and observed odds.
- Input: Cleaned odds CSV file (output from `clean_bookmaker_odds.py`)
- Output: Predicted scoring rates CSV file with home and away lambdas appended

**3. `extract_goals_reds.py`**
Extracts goal and red card minutes from raw match event files. Handles stoppage time correctly by condensing first-half stoppage time into minute 46 and second-half stoppage time into minute 92. Outputs one cleaned file per season.
- Input: Folder of raw match event Excel files (one per season, from data source)
- Output: Folder of cleaned CSV files with goal and red card minutes in wide format

**4. `combine_season_files.py`**
Combines all individual season goals/reds files into a single all-seasons file.
- Input: Folder of cleaned goals/reds CSV files (output from `extract_goals_reds.py`)
- Output: Single combined goals/reds CSV file

**5. `build_empirical_distributions.py`**
Builds the empirical minute-by-minute goal and red card distributions across all seasons. These distributions are used to scale per-match scoring rates into per-minute scoring probabilities.
- Input: Folder of cleaned goals/reds CSV files (output from `extract_goals_reds.py`)
- Output: Two CSV files — empirical goal distribution and empirical red card distribution (both covering minutes 1-92)

**6. `fix_team_names.py`**
Fixes broken character encodings and normalizes team names across seasons for Ligue 1, Bundesliga, and La Liga. This ensures team names match correctly when merging data sources.
- Input: Combined goals/reds CSV file (output from `combine_season_files.py`)
- Output: Corrected goals/reds CSV file with fixed team names and rebuilt match IDs

**7. `build_minutebyminute_dataset.py`**
Merges the predicted scoring rates, empirical goal distribution, and goals/red card data into a single minute-by-minute dataset with 92 rows per match. Also builds cumulative score and red card counters for each minute.
- Input: Predicted scoring rates CSV (output from `fit_scoring_rates.py`), combined goals/reds CSV (output from `combine_season_files.py`), empirical goal distribution CSV (output from `build_empirical_distributions.py`)
- Output: Minute-by-minute CSV file ready for live odds calculation

**8. `calculate_live_odds.py`**
Simulates minute-by-minute live betting odds using 100,000 Monte Carlo draws per game-minute. Adjusts scoring rates for red cards and produces two sets of odds: standard live odds and counterfactual no-goal-no-red odds.
- Input: Minute-by-minute CSV file (output from `build_minutebyminute_dataset.py`)
- Output: Same dataset with six new columns of live odds appended

**9. `calculate_suspense.py`**
Calculates the minute-by-minute suspense measure. Suspense at minute t captures how much the outcome probabilities would change if either team scored in minute t+1, weighted by the probability of scoring in that next minute.
- Input: Minute-by-minute CSV file with live odds (output from `calculate_live_odds.py`)
- Output: Same dataset with suspense and hypothetical probability columns appended

**10. `calculate_surprise_shock.py`**
Calculates the minute-by-minute surprise measure. Surprise captures the immediate change in outcome probabilities from one minute to the next. A shock value is calculated internally and substituted for surprise in minute 1 when a goal or red card occurs.
- Input: Minute-by-minute CSV file with suspense (output from `calculate_suspense.py`)
- Output: Same dataset with surprise column appended

**11. `calculate_league_averages.py`**
Aggregates the minute-by-minute data to game level, computes total suspense and surprise per match, and calculates league-level z-scores normalised across all seasons. Also produces season-level averages.
- Input: Minute-by-minute CSV file with surprise (output from `calculate_surprise_shock.py`)
- Output: Excel file with two sheets — Game_Results and Season_Averages

**12. `calculate_team_averages.py`**
Calculates season-by-season average suspense and surprise for each focus team and an "Other" group covering all remaining games. Run once per league by uncommenting the relevant settings block.
- Input: Game_Results sheet from league averages Excel file (output from `calculate_league_averages.py`)
- Output: Team averages CSV file with season averages per team group

**13. `build_plotting_file.py`**
Merges game-level results with season-level team averages into a single wide-format file ready for plotting. Set the `LEAGUE` variable at the top to select the league.
- Input: League averages Excel file (output from `calculate_league_averages.py`) and team averages CSV file (output from `calculate_team_averages.py`)
- Output: Wide-format CSV file with all columns needed for plots

**14. `plot_league_figures.py`**
Generates four plots per league — raw suspense, raw surprise, z-scored suspense, and z-scored surprise — showing season-by-season boxplots, scatter points, and trend lines for each focus team and the Other group. Significance stars and benchmark bands are included. Set the `LEAGUE` variable at the top to select the league.
- Input: Wide-format plotting CSV file (output from `build_plotting_file.py`)
- Output: Four PNG plots at 300 DPI

**15. `calculate_descriptives.py`**
Calculates descriptive statistics for suspense and surprise across all five leagues in four sequential steps: league-specific descriptives, global z-score standardisation, global descriptives, and minute-by-minute goal and red card distributions.
- Input: League averages Excel files from all five leagues (output from `calculate_league_averages.py`) and empirical distribution CSV files (output from `build_empirical_distributions.py`)
- Output: Three Excel files — league descriptives, global descriptives, and goal/red card distributions

---

## Random Seed

All Monte Carlo simulations use a fixed random seed of **482931** set via `np.random.seed(482931)` at the top of `calculate_live_odds.py` and `calculate_suspense.py`. This ensures that results are exactly reproducible across runs.

---

## Citation

If you use this code or methodology in your own work, please cite the original paper:

> **[Full citation to be added upon publication]**

---

## License

This repository is released under the MIT License. See `LICENSE.txt` for full details.

---

## Contact

For questions about the code or methodology, please contact:
Travis Richardson — [email to be added]
