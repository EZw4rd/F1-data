import fastf1
import pandas as pd
import os
import streamlit as st

# Setup FastF1 Cache
CACHE_DIR = 'f1_data_cache'
os.makedirs(CACHE_DIR, exist_ok=True)
fastf1.Cache.enable_cache(CACHE_DIR)

import datetime

@st.cache_data
def get_season_schedule(year: int):
    """
    Fetches the full race calendar for a given year using FastF1
    """
    try:
        schedule = fastf1.get_event_schedule(year)
        # Filter out pre-season testing
        schedule = schedule[schedule['EventFormat'] != 'testing']
        return schedule
    except Exception as e:
        st.error(f"Failed to load season schedule: {e}")
        return None

@st.cache_data
def get_season_standings(year: int):
    """
    Calculates driver and constructor standings by aggregating points from all completed sessions.
    FastF1 doesn't have a direct standings endpoint, so we calculate it.
    """
    schedule = get_season_schedule(year)
    if schedule is None: return None, None
    
    # Filter for past events (using Session5DateUtc as roughly the end of the event)
    # The 'Session5DateUtc' column often lacks timezone info in the dataframe natively, 
    # so we compare it against a timezone-naive UTC timestamp.
    now = pd.Timestamp.utcnow().tz_localize(None)
    
    # Ensure the column is also timezone-naive for a valid comparison
    session_dates = pd.to_datetime(schedule['Session5DateUtc']).dt.tz_localize(None)
    completed_events = schedule[session_dates < now]
    
    all_results = []
    
    # Let's show a progress bar in Streamlit when loading this for the first time
    progress_text = "Fetching season results..."
    with st.spinner(progress_text):
        for _, event in completed_events.iterrows():
            # Get Race Results
            try:
                race = fastf1.get_session(year, event['RoundNumber'], 'R')
                race.load(telemetry=False, weather=False, messages=False, laps=False)
                res = race.results[['BroadcastName', 'TeamName', 'Points']].copy()
                res['Round'] = event['RoundNumber']
                all_results.append(res)
                
                # Check for Sprint
                if event['EventFormat'] == 'sprint':
                    sprint = fastf1.get_session(year, event['RoundNumber'], 'S')
                    sprint.load(telemetry=False, weather=False, messages=False, laps=False)
                    sres = sprint.results[['BroadcastName', 'TeamName', 'Points']].copy()
                    sres['Round'] = event['RoundNumber'] # assign same round
                    all_results.append(sres)
            except Exception as e:
                print(f"Skipping round {event['RoundNumber']}: {e}")
                continue # Skip if session data isn't fully published yet
                
    if not all_results:
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()
        
    df = pd.concat(all_results)
    
    # 1. Aggregate drivers
    driver_standings = df.groupby(['BroadcastName', 'TeamName'])['Points'].sum().reset_index()
    driver_standings = driver_standings.sort_values(by='Points', ascending=False).reset_index(drop=True)
    driver_standings.index += 1
    
    # 2. Aggregate constructors
    constructor_standings = df.groupby('TeamName')['Points'].sum().reset_index()
    constructor_standings = constructor_standings.sort_values(by='Points', ascending=False).reset_index(drop=True)
    constructor_standings.index += 1
    
    # 3. Cumulative Points History
    # Group by driver and round, sum points (in case of sprint + race)
    points_by_round = df.groupby(['BroadcastName', 'TeamName', 'Round'])['Points'].sum().reset_index()
    # Create a full grid of Drivers x Rounds to handle DNFs/Zeros
    drivers = points_by_round['BroadcastName'].unique()
    rounds = points_by_round['Round'].unique()
    grid = pd.MultiIndex.from_product([drivers, rounds], names=['BroadcastName', 'Round']).to_frame(index=False)
    
    # Merge and fill missing rounds with 0 points
    merged = pd.merge(grid, points_by_round, on=['BroadcastName', 'Round'], how='left')
    merged['Points'] = merged['Points'].fillna(0)
    
    # Map teams back
    team_map = dict(zip(driver_standings['BroadcastName'], driver_standings['TeamName']))
    merged['TeamName'] = merged['BroadcastName'].map(team_map)
    
    # Sort and calculate cumsum
    merged = merged.sort_values(['BroadcastName', 'Round'])
    merged['CumulativePoints'] = merged.groupby('BroadcastName')['Points'].cumsum()
    
    return driver_standings, constructor_standings, merged

def format_timedelta(td, include_ms=False):
    if pd.isna(td): return None
    if isinstance(td, str): return td
    if hasattr(td, 'total_seconds'):
        ts = td.total_seconds()
        hours = int(ts // 3600)
        minutes = int((ts % 3600) // 60)
        seconds = int(ts % 60)
        if include_ms:
            ms = int(round((ts - int(ts)) * 1000))
            if hours > 0:
                return f"{hours:02d}:{minutes:02d}:{seconds:02d}.{ms:03d}"
            else:
                return f"{minutes}:{seconds:02d}.{ms:03d}"
        else:
            return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    return td

@st.cache_data
def get_session_results(year: int, round_number: int, session_type: str):
    """
    Fetches the results table for a specific session (e.g. 'R' for Race, 'Q' for Quali)
    """
    try:
        session = fastf1.get_session(year, round_number, session_type)
        session.load(telemetry=False, weather=False, messages=False, laps=False)
        
        # Format the dataframe for display
        res = session.results.copy()
        
        # Select important columns
        cols = ['Position', 'DriverNumber', 'BroadcastName', 'TeamName', 'Q1', 'Q2', 'Q3', 'Time', 'Status', 'Points', 'Abbreviation']
        available_cols = [c for c in cols if c in res.columns]
        
        display_df = res[available_cols].copy()
        
        # Convert timedelta to string if needed
        for c in ['Time', 'Q1', 'Q2', 'Q3']:
            if c in display_df.columns:
                display_df[c] = display_df[c].apply(lambda x: format_timedelta(x, include_ms=True) if pd.notnull(x) else None)
            
        return display_df, session.event
    except Exception as e:
        return None, None

@st.cache_data
def get_race_laps(year: int, round_number: int):
    """
    Fetches detailed lap-by-lap data for a race
    """
    try:
        session = fastf1.get_session(year, round_number, 'R')
        session.load(telemetry=False, weather=False, messages=False, laps=True)
        
        laps = session.laps.copy()
        
        # Convert timedeltas for easier plotting
        if not laps.empty:
            if 'LapTime' in laps.columns and laps['LapTime'].dtype == 'timedelta64[ns]':
                laps['LapTime_s'] = laps['LapTime'].dt.total_seconds()
            if 'PitInTime' in laps.columns:
                 laps['IsPitLap'] = laps['PitInTime'].notnull()
                 laps['PitInTime'] = laps['PitInTime'].apply(lambda x: format_timedelta(x, include_ms=False) if pd.notnull(x) else None)
            if 'PitOutTime' in laps.columns:
                 laps['PitOutTime'] = laps['PitOutTime'].apply(lambda x: format_timedelta(x, include_ms=False) if pd.notnull(x) else None)
                 
        return laps, session.results
    except Exception as e:
        return None, None

@st.cache_data
def get_quali_laps(year: int, round_number: int):
    """
    Fetches detailed lap-by-lap data for a Qualifying session
    """
    try:
        session = fastf1.get_session(year, round_number, 'Q')
        session.load(telemetry=False, weather=False, messages=False, laps=True)
        return session.laps.copy(), session.results
    except Exception as e:
        return None, None

@st.cache_data
def get_telemetry(year: int, round_number: int, session_type: str, driver: str, lap_number: int = None):
    """
    Fetches raw telemetry (Speed, Throttle, Brake, etc) for a specific driver.
    If lap_number is None, gets telemetry for their fastest lap.
    """
    try:
        session = fastf1.get_session(year, round_number, session_type)
        session.load(telemetry=True, weather=False, messages=False, laps=True)
        
        if lap_number:
            lap = session.laps.pick_driver(driver).pick_lap(lap_number)
        else:
            lap = session.laps.pick_driver(driver).pick_fastest()
            
        if lap is None or pd.isna(lap['LapTime']):
            return None
            
        telemetry = lap.get_telemetry()
        return telemetry
    except Exception as e:
        return None

@st.cache_data
def get_team_h2h(year: int):
    """
    Computes teammate Head-to-Head stats for races
    Returns a list of dicts with team, driver1, driver2 and their race score.
    """
    schedule = get_season_schedule(year)
    if schedule is None: return []
    
    now = pd.Timestamp.utcnow().tz_localize(None)
    session_dates = pd.to_datetime(schedule['Session5DateUtc']).dt.tz_localize(None)
    completed_events = schedule[session_dates < now]
    
    h2h_data = []
    
    with st.spinner("Calculating Teammate H2H..."):
        all_race_results = []
        for _, event in completed_events.iterrows():
            try:
                race = fastf1.get_session(year, event['RoundNumber'], 'R')
                race.load(telemetry=False, weather=False, messages=False, laps=False)
                res = race.results[['BroadcastName', 'TeamName', 'Position', 'ClassifiedPosition']].copy()
                all_race_results.append(res)
            except Exception:
                continue
                
        if not all_race_results:
            return []
            
        df = pd.concat(all_race_results)
        
        # Group by team
        for team, team_df in df.groupby('TeamName'):
            drivers = team_df['BroadcastName'].unique()
            if len(drivers) == 2:
                d1, d2 = drivers[0], drivers[1]
                
                # Compare per race (where both finished ideally, but simple position works)
                d1_wins = 0
                d2_wins = 0
                
                # Since we don't have event IDs, we sort by index blocks (each race is 20 rows)
                # A safer way: group by the chunks we appended
                
                # Actually, easier way since team_df only has 2 rows per race exactly in order:
                # We can just iterate through the races that this team participated in
                for i in range(0, len(team_df), 2):
                    race_slice = team_df.iloc[i:i+2]
                    if len(race_slice) == 2:
                        res1 = race_slice[race_slice['BroadcastName'] == d1]
                        res2 = race_slice[race_slice['BroadcastName'] == d2]
                        if not res1.empty and not res2.empty:
                            pos1 = float(res1['Position'].iloc[0])
                            pos2 = float(res2['Position'].iloc[0])
                            if pos1 < pos2:
                                d1_wins += 1
                            elif pos2 < pos1:
                                d2_wins += 1
                                
                h2h_data.append({
                    'Team': team,
                    'Driver 1': d1,
                    'D1_Score': d1_wins,
                    'Driver 2': d2,
                    'D2_Score': d2_wins
                })
                
    return h2h_data

