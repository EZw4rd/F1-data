import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from data.data_manager import get_season_schedule, get_session_results, get_quali_laps, get_telemetry
from utils.styling import get_driver_color

def render():
    st.header("🌍 Grand Prix View")
    
    year = 2026
    schedule = get_season_schedule(year)
    
    if schedule is None:
        st.error("No schedule data available.")
        return
        
    # Create a nice selectbox for the races
    events = schedule['EventName'] + " - " + schedule['Country']
    event_dict = dict(zip(events, schedule['RoundNumber']))
    
    selected_event_name = st.selectbox("Select Grand Prix:", options=list(event_dict.keys()))
    round_no = event_dict[selected_event_name]
    
    st.markdown("---")
    
    with st.spinner("Fetching Race & Qualifying Details..."):
        # Fetch Data
        race_res, event_info = get_session_results(year, round_no, 'R')
        quali_res, _ = get_session_results(year, round_no, 'Q')
        quali_laps, _ = get_quali_laps(year, round_no)
    
    if event_info is not None:
        st.subheader(f"🏁 {event_info['OfficialEventName']}")
        st.caption(f"📍 {event_info['Location']}, {event_info['Country']} | 📅 {event_info['EventDate'].strftime('%d %b %Y')}")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🏎️ Race Results")
        if race_res is not None and not race_res.empty:
            # Drop unnecessary columns for race (like Q1/Q2/Q3)
            race_display_cols = ['Position', 'DriverNumber', 'BroadcastName', 'TeamName', 'Time', 'Status', 'Points']
            race_res_display = race_res[[c for c in race_display_cols if c in race_res.columns]]
            st.dataframe(race_res_display, use_container_width=True, height=600)
        else:
            st.info("Race results are not available yet.")
            
    with col2:
        st.subheader("⏱️ Qualifying Results")
        if quali_res is not None and not quali_res.empty:
            # Drop unnecessary columns for qualifying
            display_cols = ['Position', 'DriverNumber', 'BroadcastName', 'TeamName', 'Q1', 'Q2', 'Q3']
            q_res_display = quali_res[[c for c in display_cols if c in quali_res.columns]]
            st.dataframe(q_res_display, use_container_width=True, height=600)
        else:
            st.info("Qualifying results are not available yet.")

    st.markdown("---")
    
    # --- QUALIFYING SECTOR HEATMAP ---
    st.subheader("🔥 Qualifying Sector Heatmap")
    if quali_laps is not None and not quali_laps.empty:
        # Get fastest lap for each driver
        fastest_laps = quali_laps.groupby('Driver').apply(lambda x: x.loc[x['LapTime'].idxmin()]).reset_index(drop=True)
        fastest_laps = fastest_laps.dropna(subset=['Sector1Time', 'Sector2Time', 'Sector3Time'])
        
        if not fastest_laps.empty:
            # Convert to seconds
            for col in ['Sector1Time', 'Sector2Time', 'Sector3Time']:
                fastest_laps[col] = fastest_laps[col].dt.total_seconds()
                
            # Sort by LapTime overall to order the heatmap logically (Pole to P20)
            fastest_laps['LapTime_s'] = fastest_laps['LapTime'].dt.total_seconds()
            fastest_laps = fastest_laps.sort_values('LapTime_s')
            
            # Prepare data for heatmap
            heatmap_data = fastest_laps[['Driver', 'Sector1Time', 'Sector2Time', 'Sector3Time']].set_index('Driver')
            
            fig_hm = px.imshow(
                heatmap_data,
                labels=dict(x="Sector", y="Driver", color="Time (s)"),
                x=['Sector 1', 'Sector 2', 'Sector 3'],
                text_auto=".3f",
                aspect="auto",
                color_continuous_scale="RdYlGn_r", # Reverse Red-Yellow-Green (Green is faster)
                title="Best Sector Times (Fastest Lap per Driver)"
            )
            fig_hm.update_layout(
                plot_bgcolor='#15151E',
                paper_bgcolor='#15151E',
                font=dict(color='white'),
                height=600
            )
            st.plotly_chart(fig_hm, use_container_width=True)
        else:
            st.info("Not enough sector data available to generate heatmap.")
    else:
        st.info("Qualifying laps not available.")
        
    st.markdown("---")
    
    # --- TELEMETRY COMPARISON (Q3) ---
    st.subheader("🏎️ Telemetry Overlay Comparison (Fastest Laps)")
    if quali_res is not None and not quali_res.empty:
        drivers = quali_res['BroadcastName'].tolist()
        
        col_d1, col_d2 = st.columns(2)
        with col_d1:
            d1 = st.selectbox("Driver 1", options=drivers, index=0)
        with col_d2:
            d2 = st.selectbox("Driver 2", options=drivers, index=1 if len(drivers) > 1 else 0)
            
        if d1 and d2:
            with st.spinner("Downloading Telemetry (this may take a few seconds)..."):
                # We need the 3-letter abbreviation
                code1 = quali_res[quali_res['BroadcastName'] == d1]['Abbreviation'].iloc[0]
                code2 = quali_res[quali_res['BroadcastName'] == d2]['Abbreviation'].iloc[0]
                
                team1 = quali_res[quali_res['BroadcastName'] == d1]['TeamName'].iloc[0]
                team2 = quali_res[quali_res['BroadcastName'] == d2]['TeamName'].iloc[0]
                
                t1 = get_telemetry(year, round_no, 'Q', code1)
                t2 = get_telemetry(year, round_no, 'Q', code2)
                
            if t1 is not None and t2 is not None:
                from plotly.subplots import make_subplots
                
                # Convert Distance to KM
                t1['Distance_km'] = t1['Distance'] / 1000
                t2['Distance_km'] = t2['Distance'] / 1000
                
                fig_tel = make_subplots(rows=3, cols=1, shared_xaxes=True, 
                                        vertical_spacing=0.05,
                                        subplot_titles=("Speed (km/h)", "Throttle (%)", "Brake"))
                
                color1 = get_driver_color(code1, team1)
                color2 = get_driver_color(code2, team2)
                
                # Speed
                fig_tel.add_trace(go.Scatter(x=t1['Distance_km'], y=t1['Speed'], line=dict(color=color1), name=d1), row=1, col=1)
                fig_tel.add_trace(go.Scatter(x=t2['Distance_km'], y=t2['Speed'], line=dict(color=color2), name=d2), row=1, col=1)
                
                # Throttle
                fig_tel.add_trace(go.Scatter(x=t1['Distance_km'], y=t1['Throttle'], line=dict(color=color1), showlegend=False), row=2, col=1)
                fig_tel.add_trace(go.Scatter(x=t2['Distance_km'], y=t2['Throttle'], line=dict(color=color2), showlegend=False), row=2, col=1)
                
                # Brake
                fig_tel.add_trace(go.Scatter(x=t1['Distance_km'], y=t1['Brake'], line=dict(color=color1), showlegend=False), row=3, col=1)
                fig_tel.add_trace(go.Scatter(x=t2['Distance_km'], y=t2['Brake'], line=dict(color=color2), showlegend=False), row=3, col=1)
                
                fig_tel.update_layout(
                    plot_bgcolor='#15151E',
                    paper_bgcolor='#15151E',
                    font=dict(color='white'),
                    height=800,
                    hovermode="x unified"
                )
                # Setting X axis title on the bottom subplot
                fig_tel.update_xaxes(title_text="Distance (km)", row=3, col=1)
                st.plotly_chart(fig_tel, use_container_width=True)
            else:
                st.error("Failed to load telemetry for one or both drivers. They may not have set a valid lap.")

