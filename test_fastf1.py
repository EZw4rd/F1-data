import fastf1
import os

CACHE_DIR = 'f1_data_cache'
os.makedirs(CACHE_DIR, exist_ok=True)
fastf1.Cache.enable_cache(CACHE_DIR)

schedule = fastf1.get_event_schedule(2026)
print("Schedule columns:", schedule.columns.tolist())
completed_races = schedule[schedule['EventDate'] < pd.Timestamp.now()]
print("Completed events:", len(completed_races))
