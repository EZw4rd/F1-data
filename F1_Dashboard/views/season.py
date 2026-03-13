import streamlit as st
import pandas as pd
import plotly.express as px
from data.data_manager import get_season_schedule, get_season_standings, get_team_h2h
from utils.styling import TEAM_COLORS, get_driver_color

def render():
    st.header("🏁 2026 Season View")
    
    # Select year (Hardcoded to 2026 for now, can be dynamic later)
    year = 2026
    
    # Load Data
    schedule = get_season_schedule(year)
    drivers, constructors, points_history = get_season_standings(year)
    h2h_stats = get_team_h2h(year)
    
    st.markdown("---")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("🏆 Driver Standings")
        if drivers is not None and not drivers.empty:
            
            # Simple Bar Chart for Drivers
            fig_drivers = px.bar(
                drivers, x="BroadcastName", y="Points", 
                color="TeamName", color_discrete_map=TEAM_COLORS,
                title="Driver Points"
            )
            fig_drivers.update_layout(
                plot_bgcolor='#15151E',
                paper_bgcolor='#15151E',
                font=dict(color='white'),
                showlegend=False
            )
            st.plotly_chart(fig_drivers, use_container_width=True)

            # Format display
            display_df = drivers.copy()
            st.dataframe(display_df, use_container_width=True, height=500)
        else:
            st.info("No race results available for this season yet.")
            
    with col2:
        st.subheader("🏎️ Constructor Standings")
        if constructors is not None and not constructors.empty:
            
            # Simple Bar Chart for Constructors
            fig = px.bar(
                constructors, x="TeamName", y="Points", 
                color="TeamName", color_discrete_map=TEAM_COLORS,
                title="Constructor Points"
            )
            fig.update_layout(
                plot_bgcolor='#15151E',
                paper_bgcolor='#15151E',
                font=dict(color='white'),
                showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True)
            
            st.dataframe(constructors, use_container_width=True)
        else:
            st.info("No constructor points available.")

    st.markdown("---")
    
    st.subheader("📈 Driver Championship Battle")
    if points_history is not None and not points_history.empty:
        # Create driver color map dynamically
        driver_color_map = {}
        for idx, row in points_history.drop_duplicates('BroadcastName').iterrows():
            driver_color_map[row['BroadcastName']] = TEAM_COLORS.get(row['TeamName'], '#888888')

        fig_points = px.line(
            points_history, 
            x="Round", 
            y="CumulativePoints", 
            color="BroadcastName",
            color_discrete_map=driver_color_map,
            markers=True,
            title="Cumulative Points over the Season",
            labels={"BroadcastName": "Driver", "CumulativePoints": "Points"}
        )
        fig_points.update_layout(
            plot_bgcolor='#15151E',
            paper_bgcolor='#15151E',
            font=dict(color='white'),
            height=600
        )
        st.plotly_chart(fig_points, use_container_width=True)
    else:
        st.info("No points history available yet.")
        
    st.markdown("---")
    st.subheader("⚔️ Teammate Head-to-Head (Race Finishes)")
    if h2h_stats:
        cols = st.columns(5)
        for idx, match in enumerate(h2h_stats):
            with cols[idx % 5]:
                with st.container(border=True):
                    st.caption(f"**{match['Team']}**")
                    st.markdown(f"{match['Driver 1']} **{match['D1_Score']}** - **{match['D2_Score']}** {match['Driver 2']}")
    else:
        st.info("No Head-to-Head data available yet.")

    st.markdown("---")
    st.subheader("📅 Season Calendar")
    
    if schedule is not None:
        # Create a clean display schedule
        clean_schedule = schedule[['RoundNumber', 'EventName', 'Location', 'Country', 'EventDate', 'EventFormat']].copy()
        clean_schedule['EventDate'] = pd.to_datetime(clean_schedule['EventDate']).dt.strftime('%d %b %Y')
        
        # Display as a clean list/grid using columns
        for i in range(0, len(clean_schedule), 4):
            cols = st.columns(4)
            for j in range(4):
                if i + j < len(clean_schedule):
                    event = clean_schedule.iloc[i + j]
                    with cols[j]:
                        with st.container(border=True):
                            st.markdown(f"**R{event['RoundNumber']} | {event['Country']}**")
                            st.caption(f"{event['EventName']}")
                            st.caption(f"📍 {event['Location']}")
                            st.caption(f"📅 {event['EventDate']}")
                            if event['EventFormat'] == 'sprint':
                                st.markdown("🏃‍♂️ **Sprint Weekend**")

