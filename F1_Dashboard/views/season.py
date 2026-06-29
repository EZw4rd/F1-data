import streamlit as st
import pandas as pd
import plotly.express as px
from data.data_manager import get_season_schedule, get_season_standings, get_team_h2h
from utils.styling import TEAM_COLORS, get_driver_color, apply_premium_chart_layout

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
            
            # Explicitly sort by points and set category order to prevent team grouping
            drivers_sorted = drivers.sort_values("Points", ascending=False)
            
            # Simple Bar Chart for Drivers
            fig_drivers = px.bar(
                drivers_sorted, x="BroadcastName", y="Points", 
                color="TeamName", color_discrete_map=TEAM_COLORS,
                category_orders={"BroadcastName": drivers_sorted["BroadcastName"].tolist()}
            )
            fig_drivers = apply_premium_chart_layout(fig_drivers, title="Driver Points")
            fig_drivers.update_layout(showlegend=False)
            st.plotly_chart(fig_drivers, use_container_width=True)

            # Format display
            st.dataframe(drivers_sorted, use_container_width=True, height=500)
        else:
            st.info("No race results available for this season yet.")
            
    with col2:
        st.subheader("🏎️ Constructor Standings")
        if constructors is not None and not constructors.empty:
            constructors_sorted = constructors.sort_values("Points", ascending=False)
            
            # Simple Bar Chart for Constructors
            fig = px.bar(
                constructors_sorted, x="TeamName", y="Points", 
                color="TeamName", color_discrete_map=TEAM_COLORS,
                category_orders={"TeamName": constructors_sorted["TeamName"].tolist()}
            )
            fig = apply_premium_chart_layout(fig, title="Constructor Points")
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
            
            st.dataframe(constructors_sorted, use_container_width=True)
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
            labels={"BroadcastName": "Driver", "CumulativePoints": "Points"}
        )
        fig_points = apply_premium_chart_layout(fig_points, title="Cumulative Points over the Season")
        st.plotly_chart(fig_points, use_container_width=True)
    else:
        st.info("No points history available yet.")
        
    st.markdown("---")
    st.subheader("⚔️ Teammate Head-to-Head (Race Finishes)")
    if h2h_stats:
        cols = st.columns(5)
        for idx, match in enumerate(h2h_stats):
            with cols[idx % 5]:
                html = f"""
                <div class="f1-card" style="padding: 15px; text-align: center; margin-bottom: 20px;">
                    <div style="color: #B6BABD; font-size: 0.8rem; margin-bottom: 5px;">{match['Team']}</div>
                    <div style="font-size: 1.1rem; font-family: 'Fira Code'; font-weight: bold; color: white;">
                        {match['Driver 1']} <span style="color: #E80020;">{match['D1_Score']}</span> - <span style="color: #E80020;">{match['D2_Score']}</span> {match['Driver 2']}
                    </div>
                </div>
                """
                st.markdown(html, unsafe_allow_html=True)
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
                        sprint_html = "<div style='color: #FF8000; font-size: 0.8rem; margin-top: 5px;'>🏃‍♂️ SPRINT WEEKEND</div>" if event['EventFormat'] in ['sprint', 'sprint_qualifying', 'sprint_shootout'] else ""
                        html = f"""
                        <div class="f1-card" style="margin-bottom: 20px;">
                            <div style="color: #E80020; font-weight: bold; font-size: 0.9rem;">ROUND {event['RoundNumber']} | {event['Country']}</div>
                            <div style="font-size: 1.1rem; color: white; margin-top: 5px;">{event['EventName']}</div>
                            <div style="color: #B6BABD; font-size: 0.8rem; margin-top: 5px;">📍 {event['Location']}</div>
                            <div style="color: #B6BABD; font-size: 0.8rem;">📅 {event['EventDate']}</div>
                            {sprint_html}
                        </div>
                        """
                        st.markdown(html, unsafe_allow_html=True)
