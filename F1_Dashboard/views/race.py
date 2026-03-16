import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from data.data_manager import get_season_schedule, get_race_laps
from utils.styling import TEAM_COLORS, TYRE_COLORS

def render():
    st.header("⚡ Race View")
    
    year = 2026
    schedule = get_season_schedule(year)
    
    if schedule is None:
        st.error("No schedule data available.")
        return
        
    from data.data_manager import get_latest_completed_round, SPRINT_FORMATS
    
    events = (schedule['RoundNumber'].astype(str) + ": " + schedule['EventName'] + " - " + schedule['Country']).tolist()
    event_dict = dict(zip(events, schedule['RoundNumber']))
    
    latest_round = get_latest_completed_round(schedule)
    default_idx = 0
    try:
        default_idx = list(event_dict.values()).index(latest_round)
    except (ValueError, IndexError):
        default_idx = 0

    selected_event_name = st.selectbox("Select Race:", options=events, index=default_idx, key="race_select")
    round_no = event_dict[selected_event_name]
    
    event_info_row = schedule[schedule['RoundNumber'] == round_no].iloc[0]
    is_sprint_weekend = event_info_row['EventFormat'] in SPRINT_FORMATS
    
    session_type = 'R'
    if is_sprint_weekend:
        st.info("🏃‍♂️ This is a Sprint Weekend.")
        session_choice = st.radio("Select Session:", ["Race", "Sprint"], horizontal=True)
        session_type = 'R' if session_choice == "Race" else 'S'
    
    st.markdown("---")
    
    with st.spinner(f"Processing {session_type} Lap Data (this may take a moment on first load)..."):
        # Added session_type and version parameter to force cache refresh
        laps, results, pit_stops = get_race_laps(year, round_no, session_type=session_type, reload=True)
        
    if laps is None or laps.empty:
        st.info("Lap data is not yet available for this race.")
        return
        
    # --- AUTOMATED INSIGHTS ---
    st.subheader("💡 Race Insights")
    
    insights = []
    
    # Insight 1: Fastest Lap
    if 'LapTime_s' in laps.columns:
        fastest_lap = laps.loc[laps['LapTime_s'].idxmin()]
        time_str = str(fastest_lap['LapTime']).split('days ')[-1][:9]
        insights.append(f"🟣 **Fastest Lap:** {fastest_lap['Driver']} ({time_str} on lap {fastest_lap['LapNumber']})")
        
    # Insight 2: Biggest Mover
    if not results.empty and 'GridPosition' in results.columns and 'Position' in results.columns:
        # Calculate positions gained
        res_copy = results.copy()
        res_copy['PlacesGained'] = res_copy['GridPosition'] - pd.to_numeric(res_copy['Position'], errors='coerce')
        biggest_mover = res_copy.loc[res_copy['PlacesGained'].idxmax()]
        if biggest_mover['PlacesGained'] > 0:
            insights.append(f"🚀 **Biggest Mover:** {biggest_mover['BroadcastName']} gained {int(biggest_mover['PlacesGained'])} positions (Started P{biggest_mover['GridPosition']} ➡️ Finished P{biggest_mover['Position']})")
            
    # Insight 3: Most Pit Stops or Longest Stint
    if 'Compound' in laps.columns:
        stints = laps.dropna(subset=["Compound"]).groupby(["Driver", "Stint", "Compound"])["LapNumber"].count().reset_index()
        longest_stint = stints.loc[stints['LapNumber'].idxmax()]
        insights.append(f"🛞 **Longest Stint:** {longest_stint['Driver']} ran {longest_stint['LapNumber']} laps on the {longest_stint['Compound'].upper()} compound.")
        
    if insights:
        cols = st.columns(len(insights))
        for i, insight in enumerate(insights):
            with cols[i]:
                st.info(insight)
    
    st.markdown("---")
        
    # --- LAP CHART (Position Over Time) ---
    st.subheader("📈 Driver Position Over Time")
    
    # We need to map driver abbreviations to team colors for the chart
    driver_color_map = {}
    if not results.empty:
        for idx, row in results.iterrows():
            driver_color_map[row['Abbreviation']] = TEAM_COLORS.get(row['TeamName'], '#888888')
            
    # Filter laps that have a track position
    pos_laps = laps.dropna(subset=['Position']).copy()
    
    # --- ADD LAP 0 (GRID POSITIONS) ---
    if not results.empty and 'GridPosition' in results.columns:
        grid_data = []
        for _, row in results.iterrows():
            grid_data.append({
                'LapNumber': 0,
                'Driver': row['Abbreviation'],
                'Position': row['GridPosition'],
                'Compound': 'START',
                'TyreLife': 0,
                'LapTime_s': 0
            })
        grid_df = pd.DataFrame(grid_data)
        pos_laps = pd.concat([grid_df, pos_laps], ignore_index=True)
    
    fig_pos = px.line(
        pos_laps, 
        x="LapNumber", 
        y="Position", 
        color="Driver",
        color_discrete_map=driver_color_map,
        hover_data=["Compound", "TyreLife", "LapTime_s"],
        title="Track Position (Lower is Better)"
    )
    
    fig_pos.update_yaxes(autorange="reversed", range=[20, 1]) # Invert Y axis, P1 at top
    fig_pos.update_layout(
        plot_bgcolor='#15151E',
        paper_bgcolor='#15151E',
        font=dict(color='white'),
        height=600,
        legend_title="Driver"
    )
    st.plotly_chart(fig_pos, use_container_width=True)
    
    # --- GAP TO LEADER (PACE) ---
    st.markdown("---")
    st.subheader("⏱️ Gap to Leader")
    
    if not laps.empty and 'LapTime_s' in laps.columns:
        # Calculate cumulative race time for each driver
        # We need to filter out out-laps and in-laps if we just want pure pace, but cumulative time relies on everything.
        # Assuming laps DataFrame has 'Time' which is the session time. 
        # But 'Time' is session timedelta.
        # Let's use cumulative LapTime_s per driver.
        clean_laps = laps.dropna(subset=['LapTime_s', 'Driver']).copy()
        
        # Calculate cumulative time per driver
        clean_laps['CumTime'] = clean_laps.groupby('Driver')['LapTime_s'].cumsum()
        
        # Determine the leader's cumulative time per lap
        leader_times = clean_laps.loc[clean_laps.groupby('LapNumber')['CumTime'].idxmin()]
        leader_times = leader_times[['LapNumber', 'CumTime']].rename(columns={'CumTime': 'LeaderTime'})
        
        # Merge leader times back into laps
        gap_data = pd.merge(clean_laps, leader_times, on='LapNumber')
        gap_data['GapToLeader'] = gap_data['CumTime'] - gap_data['LeaderTime']
        
        # Plot Gap
        fig_gap = px.line(
            gap_data,
            x="LapNumber",
            y="GapToLeader",
            color="Driver",
            color_discrete_map=driver_color_map,
            hover_data=["Compound", "LapTime_s"],
            title="Time relative to Race Leader (Seconds)"
        )
        # Flip Y-axis so leader (0) is at the top, and trailing drivers go down
        fig_gap.update_yaxes(autorange="reversed")
        fig_gap.update_layout(
            plot_bgcolor='#15151E',
            paper_bgcolor='#15151E',
            font=dict(color='white'),
            height=600,
            legend_title="Driver"
        )
        st.plotly_chart(fig_gap, use_container_width=True)
    else:
        st.info("Insufficient lap data to calculate gap to leader.")
    
    # --- TYRE STRATEGY TIMELINE ---
    st.markdown("---")
    st.subheader("🟡 Tyre Strategy Timeline")
    
    # Calculate stints
    stints = laps.dropna(subset=["Compound"]).groupby(["Driver", "Stint", "Compound"])["LapNumber"].agg(['min', 'max']).reset_index()
    stints = stints.rename(columns={'min': 'StartLap', 'max': 'EndLap'})
    
    # Sort drivers by their finishing position to make the chart logical
    ordered_drivers = results['Abbreviation'].tolist() if not results.empty else stints['Driver'].unique()
    
    fig_tyres = go.Figure()
    
    for driver in ordered_drivers:
        driver_stints = stints[stints["Driver"] == driver]
        for _, row in driver_stints.iterrows():
            color = TYRE_COLORS.get(str(row["Compound"]).upper(), "#808080")
            fig_tyres.add_trace(go.Bar(
                y=[driver],
                x=[row["EndLap"] - row["StartLap"] + 1],
                base=[row["StartLap"] - 1],
                orientation='h',
                name=row["Compound"],
                marker=dict(color=color, line=dict(width=1, color='black')),
                hovertemplate=f"Driver: {driver}<br>Compound: {row['Compound']}<br>Laps: {row['StartLap']} to {row['EndLap']}<extra></extra>",
                showlegend=False
            ))
            
    fig_tyres.update_layout(
        barmode='stack',
        plot_bgcolor='#15151E',
        paper_bgcolor='#15151E',
        font=dict(color='white'),
        height=700,
        yaxis={'categoryorder': 'array', 'categoryarray': ordered_drivers[::-1]} # reverse so winner is at top
    )
    st.plotly_chart(fig_tyres, use_container_width=True)
    
    # --- RACE PACE HEATMAP ---
    st.markdown("---")
    st.subheader("🔥 Race Pace Heatmap")
    
    if not laps.empty and 'LapTime_s' in laps.columns:
        # Filter realistic laps (drop crazy spikes like SC or PiT)
        pace_laps = laps.dropna(subset=['LapTime_s', 'Driver']).copy()
        # Cap outlier laps (e.g., > 130% of median lap time)
        median_lap = pace_laps['LapTime_s'].median()
        pace_laps = pace_laps[pace_laps['LapTime_s'] < (median_lap * 1.3)]
        
        # Create driver vs lap matrix
        pace_matrix = pace_laps.pivot(index='Driver', columns='LapNumber', values='LapTime_s')
        
        # Reorder drivers logically (e.g. by finishing position)
        valid_drivers = [d for d in ordered_drivers if d in pace_matrix.index]
        pace_matrix = pace_matrix.loc[valid_drivers]
        
        fig_pace = px.imshow(
            pace_matrix,
            labels=dict(x="Lap Number", y="Driver", color="Lap Time (s)"),
            aspect="auto",
            color_continuous_scale="RdYlGn_r", # Reverse: Green is faster (lower time), Red is slower
            title="Lap Times Heatmap (Filters out Pit Stops / VSC)"
        )
        fig_pace.update_layout(
            plot_bgcolor='#15151E',
            paper_bgcolor='#15151E',
            font=dict(color='white'),
            height=600
        )
        st.plotly_chart(fig_pace, use_container_width=True)
    else:
        st.info("Insufficient lap data for Pace Heatmap.")
    
    # --- PIT STOP SUMMARY ---
    st.markdown("---")
    st.subheader("🛑 Pit Stop Summary (Updated)")
    
    # Calculate pit stops from lap data
    if 'IsPitLap' in laps.columns:
        # Align PitOutTime_Raw and PitOutTime (string)
        laps['PitOutTime_Aligned_Raw'] = laps.groupby('Driver')['PitOutTime_Raw'].shift(-1)
        laps['PitOutTime_Aligned'] = laps.groupby('Driver')['PitOutTime'].shift(-1)
        
        pit_laps = laps[laps['IsPitLap'] == True].copy()
        
        if not pit_laps.empty:
            # Calculate Total Time in Pit (Lane Time)
            pit_laps['TotalTimeInPit'] = (pit_laps['PitOutTime_Aligned_Raw'] - pit_laps['PitInTime_Raw']).dt.total_seconds()
            
            # Prepare summary columns
            pit_summary = pit_laps[['Driver', 'LapNumber', 'Compound', 'PitInTime', 'PitOutTime_Aligned', 'TotalTimeInPit']].copy()
            pit_summary = pit_summary.rename(columns={
                'PitOutTime_Aligned': 'PitOutTime',
                'TotalTimeInPit': 'LaneTime (s)'
            })
            
            # Initialize Stationary Time column as N/A by default
            pit_summary['StationaryTime (s)'] = "N/A"
            
            # Merge with pit_stops for stationary duration if available
            if pit_stops is not None and not pit_stops.empty:
                try:
                    # FastF1 pit_stops 'Driver' column is usually the Driver Number (string)
                    # We need to map it to the Abbreviation (e.g. 'NOR') for our summary table
                    ps_subset = pit_stops[['Driver', 'Lap', 'Duration_s']].copy()
                    
                    # Create mapping from Results: DriverNumber -> Abbreviation
                    if results is not None and not results.empty:
                        # Ensure types match for mapping (DriverNumber is usually string or int)
                        results['DriverNumber'] = results['DriverNumber'].astype(str)
                        d_map = dict(zip(results['DriverNumber'], results['Abbreviation']))
                        
                        ps_subset['Driver'] = ps_subset['Driver'].astype(str).map(d_map)
                    
                    ps_subset = ps_subset.rename(columns={'Lap': 'LapNumber', 'Duration_s': 'Stationary_Raw'})
                    
                    # Ensure same types for merging
                    ps_subset['LapNumber'] = ps_subset['LapNumber'].astype(int)
                    pit_summary['LapNumber'] = pit_summary['LapNumber'].astype(int)
                    
                    # Merge on mapped Driver (Abbreviation) and LapNumber
                    pit_summary = pd.merge(pit_summary, ps_subset, on=['Driver', 'LapNumber'], how='left')
                    
                    # If we have merged data, fill the StationaryTime column
                    if 'Stationary_Raw' in pit_summary.columns:
                        pit_summary['StationaryTime (s)'] = pit_summary['Stationary_Raw'].map(lambda x: '{:.2f}'.format(x) if pd.notnull(x) else "N/A")
                        pit_summary = pit_summary.drop(columns=['Stationary_Raw'])
                except Exception as e:
                    pass # Keep the default "N/A"
            
            # Format LaneTime numeric column
            if 'LaneTime (s)' in pit_summary.columns:
                pit_summary['LaneTime (s)'] = pit_summary['LaneTime (s)'].map(lambda x: '{:.2f}'.format(x) if pd.notnull(x) else "N/A")

            st.dataframe(pit_summary, use_container_width=True)
        else:
            st.info("No pit stops recorded yet.")
    else:
        st.info("No pit stops available in this dataset.")
