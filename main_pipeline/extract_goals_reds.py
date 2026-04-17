# ============================================================================
# EXTRACT GOALS AND RED CARDS
# ============================================================================
# This script processes raw match event files and extracts goal and red card
# minutes for each match. It handles stoppage time correctly by condensing
# first half stoppage time into minute 46 and second half stoppage time into
# minute 92. Goals scored during red card events are removed from the goal
# list. Output is one cleaned CSV file per season with goals and red cards
# in wide format.
#
# INPUT:  Folder of raw match event Excel files (one per season)
# OUTPUT: Folder of cleaned CSV files with goal and red card minutes in wide format
# ============================================================================
 
import pandas as pd
import re
import os
import glob
from pathlib import Path
from collections import Counter
 
# ============================================================================
# SETTINGS — EDIT THESE FOR YOUR LEAGUE
# ============================================================================
 
INPUT_FOLDER  = r"path/to/your/raw_event_files"
OUTPUT_FOLDER = r"path/to/your/goals_reds_output"
 
# ============================================================================
# FUNCTIONS
# ============================================================================
 
def extract_specified_columns(input_file_path):
 
    df = pd.read_excel(input_file_path)
 
    columns_to_keep = [
        "Home_Team",
        "Home_Goals",
        "Home_Red_Cards",
        "Away_Team",
        "Away_Goals",
        "Away_Red_Cards",
        "Home_Away",
        "Event_Time",
        "Event_Half",
        "Event_Type"
    ]
 
    available_cols = [c for c in columns_to_keep if c in df.columns]
    return df[available_cols]
 
 
def transform_event_time(minute, half):
    """
    Transforms raw event times into the 92-minute match structure:
    - First half: minutes 1-45 stay as-is, 45+ stoppage time -> minute 46
    - Second half: all minutes shifted +1, 90+ stoppage time -> minute 92
    """
    minute = int(minute)
 
    if half == 1:
        if minute >= 46:
            return 46
        return minute
 
    if half == 2:
        minute += 1
        if minute > 92:
            minute = 92
        return minute
 
    return minute
 
 
def clean_and_transform_goal_string(value):
    """
    Parses goal minute strings (e.g. '23', '45+2', '90+3') and converts
    them to the 92-minute structure.
    """
    if not isinstance(value, str):
        return ''
 
    matches = re.findall(r'(\d+)(?:\+(\d+))?', value)
    adjusted_minutes = []
 
    for base, extra in matches:
        base = int(base)
 
        if extra:
            extra = int(extra)
            if base == 45:
                minute = 46
            elif base == 90:
                minute = 90 + extra
                minute += 1
                if minute > 92:
                    minute = 92
            else:
                minute = base + extra
        else:
            minute = base
            if minute > 45:
                minute += 1
                if minute > 92:
                    minute = 92
 
        adjusted_minutes.append(str(minute))
 
    return ';'.join(adjusted_minutes)
 
 
def remove_reds(goal_str, red_list):
    """
    Removes red card minutes from the goal string to avoid double counting
    events that appear in both the goals and red cards data.
    """
    if not goal_str:
        return goal_str
 
    counts = Counter(map(str, red_list))
    out = []
 
    for g in goal_str.split(';'):
        if g in counts and counts[g] > 0:
            counts[g] -= 1
        else:
            out.append(g)
 
    return ';'.join(out)
 
 
def process_all_files(input_folder, output_folder):
 
    Path(output_folder).mkdir(parents=True, exist_ok=True)
    league_files = glob.glob(os.path.join(input_folder, '*_*.xlsx'))
 
    print(f"Found {len(league_files)} files to process")
 
    for input_file_path in league_files:
 
        try:
            print(f"\nProcessing: {os.path.basename(input_file_path)}")
 
            processed_df = extract_specified_columns(input_file_path)
 
            # Apply event time transformation
            processed_df['Event_Time'] = processed_df.apply(
                lambda r: transform_event_time(r['Event_Time'], r['Event_Half']),
                axis=1
            )
 
            # Matchup + ID
            processed_df['Matchup'] = (
                processed_df['Home_Team'] + "_" + processed_df['Away_Team']
            )
            matchup_to_id = {
                m: i + 1 for i, m in enumerate(processed_df['Matchup'].unique())
            }
            processed_df['ID'] = processed_df['Matchup'].map(matchup_to_id)
 
            # Clean and transform goal strings
            processed_df['Home_Goals'] = (
                processed_df['Home_Goals'].apply(clean_and_transform_goal_string)
            )
            processed_df['Away_Goals'] = (
                processed_df['Away_Goals'].apply(clean_and_transform_goal_string)
            )
 
            # Red cards
            red_card_events = processed_df[
                processed_df['Event_Type'].isin(['Second Yellow Card', 'Red Card'])
            ]
            red_card_times = (
                red_card_events
                .groupby(['ID', 'Home_Away'])['Event_Time']
                .apply(lambda x: ';'.join(x.astype(str)))
                .unstack(fill_value='')
            )
            red_card_times.columns = [
                'Home_Reds' if c == 'Home' else 'Away_Reds'
                for c in red_card_times.columns
            ]
            red_card_times.reset_index(inplace=True)
 
            processed_df = pd.merge(processed_df, red_card_times, on='ID', how='left')
            processed_df[['Home_Reds', 'Away_Reds']] = (
                processed_df[['Home_Reds', 'Away_Reds']].fillna('')
            )
 
            # Remove red card minutes from goal strings
            red_home = (
                processed_df[
                    (processed_df['Home_Away'] == 'Home') &
                    (processed_df['Event_Type'].isin(['Red Card', 'Second Yellow Card']))
                ]
                .groupby('ID')['Event_Time'].apply(list).to_dict()
            )
            red_away = (
                processed_df[
                    (processed_df['Home_Away'] == 'Away') &
                    (processed_df['Event_Type'].isin(['Red Card', 'Second Yellow Card']))
                ]
                .groupby('ID')['Event_Time'].apply(list).to_dict()
            )
 
            processed_df['Home_Only_Goals'] = processed_df.apply(
                lambda r: remove_reds(r['Home_Goals'], red_home.get(r['ID'], [])),
                axis=1
            )
            processed_df['Away_Only_Goals'] = processed_df.apply(
                lambda r: remove_reds(r['Away_Goals'], red_away.get(r['ID'], [])),
                axis=1
            )
 
            # Year + match_id
            filename = os.path.basename(input_file_path)
            year_match = re.search(r'_(\d{4})', filename)
            year = year_match.group(1) if year_match else filename[-8:-4]
 
            processed_df['year'] = year
            processed_df['match_id'] = processed_df['year'] + "_" + processed_df['Matchup']
 
            # Wide format
            for i in range(1, 11):
                processed_df[f'homegoal{i}'] = None
                processed_df[f'awaygoal{i}'] = None
            for i in range(1, 4):
                processed_df[f'homered{i}'] = None
                processed_df[f'awayred{i}'] = None
 
            for idx, row in processed_df.iterrows():
                if row['Home_Only_Goals']:
                    for i, g in enumerate(row['Home_Only_Goals'].split(';')[:10]):
                        processed_df.at[idx, f'homegoal{i+1}'] = g
                if row['Away_Only_Goals']:
                    for i, g in enumerate(row['Away_Only_Goals'].split(';')[:10]):
                        processed_df.at[idx, f'awaygoal{i+1}'] = g
                if row['Home_Reds']:
                    for i, r in enumerate(row['Home_Reds'].split(';')[:3]):
                        processed_df.at[idx, f'homered{i+1}'] = r
                if row['Away_Reds']:
                    for i, r in enumerate(row['Away_Reds'].split(';')[:3]):
                        processed_df.at[idx, f'awayred{i+1}'] = r
 
            processed_df_unique = processed_df.drop_duplicates(subset=['ID'], keep='first')
 
            # Column ordering
            home_goal_cols = [f'homegoal{i}' for i in range(1, 11)]
            away_goal_cols = [f'awaygoal{i}' for i in range(1, 11)]
            home_red_cols  = [f'homered{i}'  for i in range(1, 4)]
            away_red_cols  = [f'awayred{i}'  for i in range(1, 4)]
 
            base_cols = [
                c for c in processed_df_unique.columns
                if c not in home_goal_cols + away_goal_cols + home_red_cols + away_red_cols
            ]
            ordered_cols = base_cols + home_goal_cols + away_goal_cols + home_red_cols + away_red_cols
            processed_df_unique = processed_df_unique[ordered_cols]
 
            # Save as CSV
            output_filename = (
                os.path.basename(input_file_path).replace('.xlsx', '_goals_reds.csv')
            )
            processed_df_unique.to_csv(
                os.path.join(output_folder, output_filename), index=False
            )
            print(f"Saved: {output_filename}")
 
        except Exception as e:
            print(f"Error processing {os.path.basename(input_file_path)}: {e}")
 
    print(f"\nProcessing complete! Files saved to: {output_folder}")
 
# ============================================================================
# RUN SCRIPT
# ============================================================================
 
process_all_files(INPUT_FOLDER, OUTPUT_FOLDER)