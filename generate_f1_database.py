import fastf1
import pandas as pd
import os
import sys

# Setup FastF1 Cache
cache_dir = 'f1_data_cache'
os.makedirs(cache_dir, exist_ok=True)
fastf1.Cache.enable_cache(cache_dir)

# Load 2026 Australian GP Race and Qualifying
year = 2026
gp = 'Australia'

print(f"Loading {year} {gp} Race session...")
race = fastf1.get_session(year, gp, 'R')
race.load(telemetry=False, weather=True, messages=False)

print(f"Loading {year} {gp} Qualifying session...")
quali = fastf1.get_session(year, gp, 'Q')
quali.load(telemetry=False, weather=False, messages=False)

output_file = 'f1_2026_australia_database.xlsx'

print(f"Generating Database: {output_file}")
with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
    # 1. Race Laps DataFrame
    race_laps = race.laps.copy()
    
    # Clean up un-exportable columns like Pickled data
    for col in race_laps.columns:
        if race_laps[col].dtype == 'timedelta64[ns]':
            # Convert timedelta to seconds for easier Excel viewing
            race_laps[col] = race_laps[col].dt.total_seconds()
            
    # Save Race Laps
    race_laps.to_excel(writer, sheet_name='Race Laps', index=False)
    
    # 2. Race Results DataFrame
    results = race.results.copy()
    # Convert timedeltas in results
    if 'Time' in results.columns and results['Time'].dtype == 'timedelta64[ns]':
         results['Time'] = results['Time'].dt.total_seconds()
    results.to_excel(writer, sheet_name='Race Results', index=False)
    
    # 3. Qualifying Laps
    quali_laps = quali.laps.copy()
    for col in quali_laps.columns:
        if quali_laps[col].dtype == 'timedelta64[ns]':
            quali_laps[col] = quali_laps[col].dt.total_seconds()
    quali_laps.to_excel(writer, sheet_name='Qualifying Laps', index=False)
    
    # 4. Weather Data
    weather = race.weather_data.copy()
    if 'Time' in weather.columns and weather['Time'].dtype == 'timedelta64[ns]':
        weather['Time'] = weather['Time'].dt.total_seconds()
    weather.to_excel(writer, sheet_name='Race Weather', index=False)

print(f"Database successfully saved to {output_file}")
