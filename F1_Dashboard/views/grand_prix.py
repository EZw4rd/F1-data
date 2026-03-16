import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from data.data_manager import get_season_schedule, get_session_results, get_quali_laps, get_telemetry, get_latest_completed_round, SPRINT_FORMATS
from utils.styling import get_driver_color

def render():
    st.header("🌍 Grand Prix View")
    
    year = 2026
    schedule = get_season_schedule(year)
    
    if schedule is None:
        st.error("No schedule data available.")
        return
        
    # Create a nice selectbox for the races
    events = (schedule['RoundNumber'].astype(str) + ": " + schedule['EventName'] + " - " + schedule['Country']).tolist()
    event_dict = dict(zip(events, schedule['RoundNumber']))
    
    latest_round = get_latest_completed_round(schedule)
    default_idx = 0
    try:
        default_idx = list(event_dict.values()).index(latest_round)
    except (ValueError, IndexError):
        default_idx = 0

    selected_event_name = st.selectbox("Select Grand Prix:", options=events, index=default_idx)
    round_no = event_dict[selected_event_name]
    
    event_info_row = schedule[schedule['RoundNumber'] == round_no].iloc[0]
    is_sprint_weekend = event_info_row['EventFormat'] in SPRINT_FORMATS
    
    # --- TRACK OVERVIEW ---
    from data.track_info import get_track_info
    t_info = get_track_info(event_info_row['EventName'])
    
    if t_info:
        with st.expander(f"📖 Track Overview: {t_info['CircuitName']}", expanded=True):
            c1, c2, c3 = st.columns(3)
            c1.metric("📏 Length", f"{t_info['Length_km']} km")
            c2.metric("🔁 Turns", t_info['Turns'])
            c3.metric("🚀 2026 Zones", "5 Straight / 1 Ovt k" if "Australia" in event_info_row['EventName'] else "4 Straight / 1 Ovt k")
            
            st.markdown(f"**💡 Key Characteristics:**")
            st.write(", ".join(t_info['Characteristics']))
            
            st.markdown(f"**🏁 Overtaking Difficulty:** {t_info['Overtaking']}")
            st.markdown(f"**📈 Strategic Insights:** {t_info['Strategy']}")
            st.info(f"✨ **Fun Fact:** {t_info['FunFact']}")

    # --- SESSION SELECTOR FOR SPRINT WEEKENDS ---
    view_mode = "Main Race"
    if is_sprint_weekend:
        st.info("🏃‍♂️ This is a Sprint Weekend.")
        view_mode = st.radio("Select Focused View:", ["Main Race", "Sprint"], horizontal=True)

    st.markdown("---")
    
    with st.spinner(f"Fetching {view_mode} Details..."):
        # Fetch shared/main data
        race_res, event_info = get_session_results(year, round_no, 'R')
        quali_res, _ = get_session_results(year, round_no, 'Q')
        quali_laps, _ = get_quali_laps(year, round_no)
        
        # Switch based on view mode
        if view_mode == "Sprint" and is_sprint_weekend:
            sprint_res, _ = get_session_results(year, round_no, 'S')
            sq_res, _ = get_session_results(year, round_no, 'SQ')
            # If SQ is not found, try SS (Sprint Shootout)
            if sq_res is None or sq_res.empty:
                sq_res, _ = get_session_results(year, round_no, 'SS')
            
            from data.data_manager import fastf1
            try:
                s_session = fastf1.get_session(year, round_no, 'S')
                s_session.load(telemetry=False, weather=False, messages=False, laps=True)
                sprint_laps = s_session.laps.copy()
            except:
                sprint_laps = pd.DataFrame()

            # --- RENDER SPRINT VIEW ---
            if event_info is not None:
                st.subheader(f"🏁 {event_info['OfficialEventName']} - SPRINT")
                st.caption(f"📍 {event_info['Location']}, {event_info['Country']} | 📅 {event_info['EventDate'].strftime('%d %b %Y')}")
            
            col_s1, col_s2 = st.columns(2)
            with col_s1:
                st.subheader("🏃‍♂️ Sprint Results")
                if sprint_res is not None and not sprint_res.empty:
                    s_cols = ['Position', 'DriverNumber', 'BroadcastName', 'TeamName', 'Time', 'Status', 'Points']
                    st.dataframe(sprint_res[[c for c in s_cols if c in sprint_res.columns]], use_container_width=True, height=500)
                else:
                    st.info("Sprint results N/A.")
            
            with col_s2:
                st.subheader("⏱️ Sprint Qualifying Results")
                if sq_res is not None and not sq_res.empty:
                    sq_cols = ['Position', 'DriverNumber', 'BroadcastName', 'TeamName', 'Q1', 'Q2', 'Q3']
                    st.dataframe(sq_res[[c for c in sq_cols if c in sq_res.columns]], use_container_width=True, height=500)
                else:
                    st.info("Sprint Qualifying results N/A.")

            if not sprint_laps.empty:
                st.markdown("---")
                st.subheader("🔥 Sprint Sector Heatmap")
                try:
                    s_fastest = sprint_laps.groupby('Driver', group_keys=False).apply(lambda x: x.loc[x['LapTime'].idxmin()]).reset_index(drop=True)
                    s_fastest = s_fastest.dropna(subset=['Sector1Time', 'Sector2Time', 'Sector3Time'])
                    if not s_fastest.empty:
                        for col in ['Sector1Time', 'Sector2Time', 'Sector3Time']:
                            s_fastest[col] = s_fastest[col].dt.total_seconds()
                        s_fastest['LapTime_s'] = s_fastest['LapTime'].dt.total_seconds()
                        s_fastest = s_fastest.sort_values('LapTime_s')
                        hm_data = s_fastest[['Driver', 'Sector1Time', 'Sector2Time', 'Sector3Time']].set_index('Driver')
                        fig = px.imshow(hm_data, labels=dict(x="Sector", y="Driver", color="Time (s)"), x=['S1', 'S2', 'S3'], text_auto=".3f", aspect="auto", color_continuous_scale="RdYlGn_r")
                        fig.update_layout(plot_bgcolor='#15151E', paper_bgcolor='#15151E', font=dict(color='white'), height=500)
                        st.plotly_chart(fig, use_container_width=True)
                except:
                    st.info("Heatmap N/A.")
        
        else:
            # --- RENDER MAIN RACE VIEW ---
            if event_info is not None:
                st.subheader(f"🏁 {event_info['OfficialEventName']}")
                st.caption(f"📍 {event_info['Location']}, {event_info['Country']} | 📅 {event_info['EventDate'].strftime('%d %b %Y')}")

            col1, col2 = st.columns(2)
            with col1:
                st.subheader("🏎️ Race Results")
                if race_res is not None and not race_res.empty:
                    st.dataframe(race_res[['Position', 'DriverNumber', 'BroadcastName', 'TeamName', 'Time', 'Status', 'Points']], use_container_width=True, height=500)
                else:
                    st.info("Race results N/A.")
            with col2:
                st.subheader("⏱️ Qualifying Results")
                if quali_res is not None and not quali_res.empty:
                    st.dataframe(quali_res[['Position', 'DriverNumber', 'BroadcastName', 'TeamName', 'Q1', 'Q2', 'Q3']], use_container_width=True, height=500)
                else:
                    st.info("Quali results N/A.")

            if quali_laps is not None and not quali_laps.empty:
                st.markdown("---")
                st.subheader("🔥 Qualifying Sector Heatmap")
                try:
                    q_fastest = quali_laps.groupby('Driver', group_keys=False).apply(lambda x: x.loc[x['LapTime'].idxmin()]).reset_index(drop=True)
                    q_fastest = q_fastest.dropna(subset=['Sector1Time', 'Sector2Time', 'Sector3Time'])
                    if not q_fastest.empty:
                        for col in ['Sector1Time', 'Sector2Time', 'Sector3Time']:
                            q_fastest[col] = q_fastest[col].dt.total_seconds()
                        q_fastest['LapTime_s'] = q_fastest['LapTime'].dt.total_seconds()
                        q_fastest = q_fastest.sort_values('LapTime_s')
                        hm_data = q_fastest[['Driver', 'Sector1Time', 'Sector2Time', 'Sector3Time']].set_index('Driver')
                        fig = px.imshow(hm_data, labels=dict(x="Sector", y="Driver", color="Time (s)"), x=['S1', 'S2', 'S3'], text_auto=".3f", aspect="auto", color_continuous_scale="RdYlGn_r")
                        fig.update_layout(plot_bgcolor='#15151E', paper_bgcolor='#15151E', font=dict(color='white'), height=600)
                        st.plotly_chart(fig, use_container_width=True)
                except:
                    st.info("Heatmap N/A.")

            # --- TELEMETRY ---
            st.markdown("---")
            st.subheader("🏎️ Telemetry Overlay Comparison (Qualifying)")
            if quali_res is not None and not quali_res.empty:
                drivers = quali_res['BroadcastName'].tolist()
                c1, c2 = st.columns(2)
                d1 = c1.selectbox("Driver 1", options=drivers, index=0)
                d2 = c2.selectbox("Driver 2", options=drivers, index=1 if len(drivers) > 1 else 0)
                if d1 and d2:
                    with st.spinner("Downloading Telemetry..."):
                        info1 = quali_res[quali_res['BroadcastName'] == d1].iloc[0]
                        info2 = quali_res[quali_res['BroadcastName'] == d2].iloc[0]
                        t1 = get_telemetry(year, round_no, 'Q', info1['Abbreviation'])
                        t2 = get_telemetry(year, round_no, 'Q', info2['Abbreviation'])
                        if t1 is not None and t2 is not None:
                            from plotly.subplots import make_subplots
                            t1['Distance_km'] = t1['Distance'] / 1000
                            t2['Distance_km'] = t2['Distance'] / 1000
                            fig = make_subplots(rows=3, cols=1, shared_xaxes=True, vertical_spacing=0.05, subplot_titles=("Speed (km/h)", "Throttle (%)", "Brake"))
                            col1 = get_driver_color(info1['Abbreviation'], info1['TeamName'])
                            col2 = get_driver_color(info2['Abbreviation'], info2['TeamName'])
                            fig.add_trace(go.Scatter(x=t1['Distance_km'], y=t1['Speed'], line=dict(color=col1), name=d1), row=1, col=1)
                            fig.add_trace(go.Scatter(x=t2['Distance_km'], y=t2['Speed'], line=dict(color=col2), name=d2), row=1, col=1)
                            fig.add_trace(go.Scatter(x=t1['Distance_km'], y=t1['Throttle'], line=dict(color=col1), showlegend=False), row=2, col=1)
                            fig.add_trace(go.Scatter(x=t2['Distance_km'], y=t2['Throttle'], line=dict(color=col2), showlegend=False), row=2, col=1)
                            fig.add_trace(go.Scatter(x=t1['Distance_km'], y=t1['Brake'], line=dict(color=col1), showlegend=False), row=3, col=1)
                            fig.add_trace(go.Scatter(x=t2['Distance_km'], y=t2['Brake'], line=dict(color=col2), showlegend=False), row=3, col=1)
                            fig.update_layout(plot_bgcolor='#15151E', paper_bgcolor='#15151E', font=dict(color='white'), height=800, hovermode="x unified")
                            fig.update_xaxes(title_text="Distance (km)", row=3, col=1)
                            st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.caption("Data provided by FastF1")
