# ============================================================================
# PLOT LEAGUE FIGURES
# ============================================================================
# This script generates four plots per league:
#   1. Suspense (raw)
#   2. Surprise (raw)
#   3. Suspense (z-score)
#   4. Surprise (z-score)
#
# Each plot shows season-by-season boxplots and scatter points for each
# focus team and the "Other" group, with trend lines connecting seasonal
# means. Significance stars are shown above the relevant team/season
# combinations. A benchmark band is shown for raw suspense and surprise.
#
# Run this script once per league by setting the LEAGUE variable below.
#
# INPUT:  Plotting file (output of build_plotting_file.py)
# OUTPUT: Four PNG plots saved to the league's Plots folder
# ============================================================================

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# ============================================================================
# SETTINGS - SET YOUR LEAGUE HERE
# ============================================================================

LEAGUE = "EPL"   # Options: "EPL", "Ligue1", "Bundesliga", "SerieA", "LaLiga"

# ============================================================================
# LEAGUE CONFIGURATIONS
# ============================================================================

LEAGUE_CONFIG = {
    "EPL": {
        "input_file": r"path/to/England_Men/Final/EPL_Final_plotting_file.xlsx",
        "output_dir": r"path/to/England_Men/Plots",
        "focus_teams": {
            "Manchester City": ("city",      "blue"),
            "Arsenal":         ("arsenal",   "red"),
            "Liverpool":       ("liverpool", "limegreen"),
        },
        "significance_suspense": {
            2010: {'Arsenal'},
            2011: {'Manchester City', 'Other Teams'},
            2012: set(),
            2013: {'Manchester City', 'Liverpool', 'Arsenal'},
            2014: {'Manchester City', 'Arsenal'},
            2015: {'Manchester City'},
            2016: {'Manchester City', 'Arsenal', 'Other Teams'},
            2017: {'Manchester City', 'Liverpool', 'Arsenal'},
            2018: {'Manchester City', 'Liverpool', 'Arsenal', 'Other Teams'},
            2019: {'Manchester City', 'Liverpool'},
            2020: {'Manchester City'},
            2021: {'Manchester City', 'Liverpool', 'Arsenal'},
            2022: {'Manchester City', 'Arsenal'},
            2023: {'Manchester City', 'Arsenal', 'Other Teams'},
        },
        "significance_surprise": {
            2010: set(),
            2011: set(),
            2012: set(),
            2013: {'Arsenal'},
            2014: set(),
            2015: set(),
            2016: set(),
            2017: {'Manchester City'},
            2018: {'Manchester City', 'Liverpool'},
            2019: set(),
            2020: {'Manchester City'},
            2021: {'Manchester City'},
            2022: {'Manchester City'},
            2023: set(),
        },
    },

    "Ligue1": {
        "input_file": r"path/to/France_Men/Final/Ligue1_Final_plotting_file.xlsx",
        "output_dir": r"path/to/France_Men/Plots",
        "focus_teams": {
            "Paris Saint-Germain": ("psg",       "darkblue"),
            "Lyon":                ("lyon",      "gold"),
            "Marseille":           ("marseille", "skyblue"),
        },
        "significance_suspense": {
            2010: set(),
            2011: set(),
            2012: set(),
            2013: {'Paris Saint-Germain'},
            2014: {'Paris Saint-Germain'},
            2015: {'Paris Saint-Germain'},
            2016: {'Paris Saint-Germain'},
            2017: {'Paris Saint-Germain', 'Lyon', 'Marseille'},
            2018: {'Paris Saint-Germain'},
            2019: {'Paris Saint-Germain'},
            2020: {'Paris Saint-Germain'},
            2021: {'Paris Saint-Germain', 'Lyon'},
            2022: {'Paris Saint-Germain'},
            2023: {'Paris Saint-Germain'},
        },
        "significance_surprise": {
            2010: set(),
            2011: set(),
            2012: set(),
            2013: set(),
            2014: set(),
            2015: {'Paris Saint-Germain'},
            2016: {'Paris Saint-Germain'},
            2017: {'Paris Saint-Germain'},
            2018: set(),
            2019: set(),
            2020: {'Paris Saint-Germain'},
            2021: set(),
            2022: set(),
            2023: set(),
        },
    },

    "Bundesliga": {
        "input_file": r"path/to/Germany_Men/Final/Bundesliga_Final_plotting_file.xlsx",
        "output_dir": r"path/to/Germany_Men/Plots",
        "focus_teams": {
            "Bayern Munich":    ("bayern",     "red"),
            "Dortmund":         ("dortmund",   "gold"),
            "Bayer Leverkusen": ("leverkusen", "darkred"),
        },
        "significance_suspense": {
            2010: {'Bayern Munich', 'Dortmund'},
            2011: {'Bayern Munich', 'Dortmund'},
            2012: {'Bayern Munich', 'Dortmund'},
            2013: {'Bayern Munich', 'Dortmund'},
            2014: {'Bayern Munich'},
            2015: {'Bayern Munich', 'Dortmund'},
            2016: {'Bayern Munich'},
            2017: {'Bayern Munich'},
            2018: {'Bayern Munich', 'Bayer Leverkusen'},
            2019: {'Bayern Munich', 'Dortmund'},
            2020: {'Bayern Munich'},
            2021: {'Bayern Munich', 'Dortmund'},
            2022: {'Bayern Munich', 'Dortmund'},
            2023: {'Bayern Munich', 'Bayer Leverkusen'},
        },
        "significance_surprise": {
            2010: set(),
            2011: {'Bayern Munich'},
            2012: {'Bayern Munich'},
            2013: {'Bayern Munich'},
            2014: {'Bayern Munich'},
            2015: {'Bayern Munich'},
            2016: set(),
            2017: {'Bayern Munich'},
            2018: {'Bayern Munich'},
            2019: {'Bayern Munich'},
            2020: set(),
            2021: {'Bayern Munich'},
            2022: {'Bayern Munich'},
            2023: set(),
        },
    },

    "SerieA": {
        "input_file": r"path/to/Italy_Men/Final/SerieA_Final_plotting_file.xlsx",
        "output_dir": r"path/to/Italy_Men/Plots",
        "focus_teams": {
            "Juventus":       ("juventus", "black"),
            "Napoli":         ("napoli",   "cyan"),
            "Internazionale": ("inter",    "blue"),
        },
        "significance_suspense": {
            2010: set(),
            2011: set(),
            2012: {'Juventus'},
            2013: {'Juventus', 'Napoli'},
            2014: {'Juventus'},
            2015: {'Juventus', 'Napoli'},
            2016: {'Juventus', 'Napoli'},
            2017: {'Juventus', 'Napoli'},
            2018: {'Juventus', 'Napoli'},
            2019: {'Juventus', 'Internazionale'},
            2020: {'Juventus', 'Napoli', 'Internazionale'},
            2021: {'Internazionale'},
            2022: {'Napoli'},
            2023: {'Internazionale'},
        },
        "significance_surprise": {
            2010: set(),
            2011: {'Juventus'},
            2012: set(),
            2013: {'Juventus'},
            2014: set(),
            2015: {'Napoli'},
            2016: {'Juventus'},
            2017: set(),
            2018: set(),
            2019: set(),
            2020: set(),
            2021: set(),
            2022: set(),
            2023: {'Internazionale'},
        },
    },

    "LaLiga": {
        "input_file": r"path/to/Spain_Men/Final/LaLiga_Final_plotting_file.xlsx",
        "output_dir": r"path/to/Spain_Men/Plots",
        "focus_teams": {
            "Real Madrid":     ("realmadrid", "purple"),
            "Barcelona":       ("barcelona",  "darkblue"),
            "Atlético Madrid": ("atletico",   "red"),
        },
        "significance_suspense": {
            2010: {'Real Madrid', 'Barcelona', 'Atlético Madrid'},
            2011: {'Real Madrid', 'Barcelona'},
            2012: {'Real Madrid', 'Barcelona'},
            2013: {'Real Madrid', 'Barcelona', 'Atlético Madrid'},
            2014: {'Real Madrid', 'Barcelona', 'Atlético Madrid'},
            2015: {'Real Madrid', 'Barcelona', 'Atlético Madrid'},
            2016: {'Real Madrid', 'Barcelona', 'Atlético Madrid'},
            2017: {'Real Madrid', 'Barcelona'},
            2018: {'Real Madrid', 'Barcelona'},
            2019: {'Barcelona'},
            2020: {'Barcelona'},
            2021: set(),
            2022: {'Barcelona'},
            2023: {'Real Madrid', 'Atlético Madrid'},
        },
        "significance_surprise": {
            2010: {'Real Madrid', 'Barcelona'},
            2011: {'Real Madrid', 'Barcelona'},
            2012: set(),
            2013: {'Atlético Madrid'},
            2014: {'Real Madrid', 'Barcelona', 'Atlético Madrid'},
            2015: {'Real Madrid', 'Barcelona'},
            2016: set(),
            2017: set(),
            2018: set(),
            2019: set(),
            2020: set(),
            2021: set(),
            2022: {'Barcelona'},
            2023: set(),
        },
    },
}

# ============================================================================
# BENCHMARK BANDS (same for all leagues)
# ============================================================================

BENCHMARK_BANDS = {
    'suspense': (6.08, 6.70),
    'surprise': (1.34, 1.99),
}

# ============================================================================
# LOAD CONFIG AND DATA
# ============================================================================

config      = LEAGUE_CONFIG[LEAGUE]
focus_teams = config["focus_teams"]
other_color = 'black'

os.makedirs(config["output_dir"], exist_ok=True)

df = pd.read_excel(config["input_file"])
df['season_label'] = 2000 + df['season'].astype(str).str[:2].astype(int)

# ============================================================================
# TEAM CATEGORIZATION
# ============================================================================

def categorize_team(row):
    for team in focus_teams:
        if row['home_team'] == team or row['away_team'] == team:
            return team
    return 'Other Teams'

df['Team_Category'] = df.apply(categorize_team, axis=1)

# ============================================================================
# BUILD TEAM COLOR MAP (for significance stars)
# ============================================================================

team_colors = {team: color for team, (_, color) in focus_teams.items()}
team_colors['Other Teams'] = other_color

# ============================================================================
# METRICS TO PLOT
# ============================================================================

metrics = [
    ('suspense',   'average_suspense',   f'{LEAGUE} Match Suspense',           f'{LEAGUE}_suspense.png',   config["significance_suspense"]),
    ('surprise',   'average_surprise',   f'{LEAGUE} Match Surprise',           f'{LEAGUE}_surprise.png',   config["significance_surprise"]),
    ('suspense_z', 'average_suspense_z', f'{LEAGUE} Match Suspense (Z-score)', f'{LEAGUE}_suspense_z.png', None),
    ('surprise_z', 'average_surprise_z', f'{LEAGUE} Match Surprise (Z-score)', f'{LEAGUE}_surprise_z.png', None),
]

# ============================================================================
# PLOTTING LOOP
# ============================================================================

for value_col, avg_suffix, title, filename, significance in metrics:

    fig, ax = plt.subplots(figsize=(18, 8))

    unique_years = np.unique(df['season_label'])
    positions    = np.arange(0, len(unique_years) * 2, 2)
    box_width    = 0.2
    alpha        = 0.5

    # --- Benchmark band ---
    if value_col in BENCHMARK_BANDS:
        band_low, band_high = BENCHMARK_BANDS[value_col]
        ax.axhspan(band_low, band_high, color='grey', alpha=0.25, zorder=0)

    team_positions = {}

    # --- Focus teams ---
    for idx, (team, (prefix, color)) in enumerate(focus_teams.items()):
        team_data    = df[df['Team_Category'] == team]
        box_positions = positions + idx * box_width - box_width
        team_positions[team] = dict(zip(unique_years, box_positions))

        data_by_year = [
            team_data[team_data['season_label'] == year][value_col].values
            for year in unique_years
        ]

        ax.boxplot(
            data_by_year,
            positions=box_positions,
            widths=box_width,
            patch_artist=True,
            boxprops=dict(facecolor=color, color=color, alpha=alpha),
            whiskerprops=dict(color=color),
            capprops=dict(color=color),
            medianprops=dict(color='black'),
            flierprops=dict(markerfacecolor=color, marker='o', markersize=5, linestyle='none')
        )

        for year, pos in zip(unique_years, box_positions):
            y_data = team_data[team_data['season_label'] == year][value_col]
            ax.scatter(np.full(y_data.shape, pos), y_data, color=color, alpha=0.7, s=10)

        avg_col  = f'{prefix}_{avg_suffix}'
        avg_data = (
            df[df['Team_Category'] == team]
            .groupby('season_label')[avg_col]
            .mean()
        )
        ax.plot(box_positions, avg_data.values, color=color, linewidth=2, label=team)

    # --- Other teams ---
    other_positions = positions + len(focus_teams) * box_width - box_width
    team_positions['Other Teams'] = dict(zip(unique_years, other_positions))
    other_data = df[df['Team_Category'] == 'Other Teams']

    data_by_year = [
        other_data[other_data['season_label'] == year][value_col].values
        for year in unique_years
    ]

    ax.boxplot(
        data_by_year,
        positions=other_positions,
        widths=box_width,
        patch_artist=True,
        boxprops=dict(facecolor=other_color, color=other_color, alpha=alpha),
        whiskerprops=dict(color=other_color),
        capprops=dict(color=other_color),
        medianprops=dict(color='black'),
        flierprops=dict(markerfacecolor=other_color, marker='o', markersize=5, linestyle='none')
    )

    for year, pos in zip(unique_years, other_positions):
        y_data = other_data[other_data['season_label'] == year][value_col]
        ax.scatter(np.full(y_data.shape, pos), y_data, color=other_color, alpha=0.7, s=10)

    other_avg_col = f'other_{avg_suffix}'
    other_avg     = (
        df[df['Team_Category'] == 'Other Teams']
        .groupby('season_label')[other_avg_col]
        .mean()
    )
    ax.plot(other_positions, other_avg.values, color=other_color, linewidth=2, label='Other Teams')

    # --- Significance stars ---
    if significance is not None:
        y_min, y_max = ax.get_ylim()
        ax.set_ylim(y_min, y_max * 1.12)
        y_min, y_max = ax.get_ylim()
        y_range = y_max - y_min

        for year, starred_teams in significance.items():
            if year not in unique_years:
                continue
            for team_name in starred_teams:
                if team_name not in team_positions:
                    continue
                x_pos      = team_positions[team_name][year]
                star_color = team_colors.get(team_name, 'black')
                ax.text(
                    x_pos, y_max - y_range * 0.01,
                    '*',
                    ha='center', va='top',
                    fontsize=18, color=star_color,
                    fontweight='bold', zorder=10
                )

    # --- Axes and labels ---
    ax.set_title(title)
    ax.set_xlabel('Season')
    ax.set_ylabel(title)
    ax.legend(loc='upper right', bbox_to_anchor=(1, 0.98), bbox_transform=ax.transAxes)
    ax.grid(True)
    ax.set_xticks(positions)
    ax.set_xticklabels(unique_years, rotation=45)

    if value_col.endswith('_z'):
        ax.set_ylim(-3, 3)

    fig.subplots_adjust(top=0.92, bottom=0.15)

    plt.savefig(
        os.path.join(config["output_dir"], filename),
        dpi=300,
        bbox_inches='tight'
    )
    plt.close()

    print(f"  Saved: {filename}")

print(f"\n All 4 {LEAGUE} plots created successfully.")