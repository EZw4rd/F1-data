import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from data.data_manager import get_season_schedule, get_race_laps
from utils.styling import TEAM_COLORS, TYRE_COLORS

def render():
    st.header("🚦 Race View")
    
    year = 2026
    schedule = get_season_schedule(year)
    
    if schedule is None:
        st.error("No schedule data available.")
        return
        
    events = schedule['EventName'] + " - " + schedule['Country']
    event_dict = dict(zip(events, schedule['RoundNumber']))
    
    selected_event_name = st.selectbox("Select Race:", options=list(event_dict.keys()), key="race_select")
    round_no = event_dict[selected_event_name]
    
    st.markdown("---")
    
    with st.spinner("Processing Lap Data (this may take a moment on first load)..."):
        laps, results = get_race_laps(year, round_no)
        
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
    st.subheader("🛑 Pit Stop Summary")
    
    # Calculate pit stops from lap data
    if 'IsPitLap' in laps.columns and 'PitOutTime' in laps.columns:
        # PitOutTime is recorded on the OUT lap (the lap after the IN lap)
        # Align it by shifting backwards per driver
        laps['PitOutTime_Aligned'] = laps.groupby('Driver')['PitOutTime'].shift(-1)
        
        pit_laps = laps[laps['IsPitLap'] == True].copy()
        if not pit_laps.empty:
            pit_summary = pit_laps[['Driver', 'LapNumber', 'Compound', 'PitInTime', 'PitOutTime_Aligned']].copy()
            pit_summary = pit_summary.rename(columns={'PitOutTime_Aligned': 'PitOutTime'})
            st.dataframe(pit_summary, use_container_width=True)
        else:
            st.info("No pit stops recorded yet.")
    else:
        st.info("No pit stops available in this dataset.")
