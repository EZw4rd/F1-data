import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# Page Config
st.set_page_config(page_title="F1 Data Dashboard", page_icon="🏎️", layout="wide")

# Title and Description
st.title("🏎️ Formula 1 Analytics Dashboard: 2026 Australian Grand Prix")
st.markdown("Interactive analysis of lap times, tyre strategies, and race pace based on the generated Excel Database.")

@st.cache_data
def load_data():
    excel_path = "f1_2026_australia_database.xlsx"
    laps = pd.read_excel(excel_path, sheet_name="Race Laps")
    results = pd.read_excel(excel_path, sheet_name="Race Results")
    return laps, results

try:
    laps, results = load_data()
except Exception as e:
    st.error(f"Could not load database. Run `python generate_f1_database.py` first. Error: {str(e)}")
    st.stop()

# Filter out inaccurate laps (like in/out laps, VSC)
accurate_laps = laps[(laps["IsAccurate"] == True)]

st.sidebar.header("Filter Options")
selected_drivers = st.sidebar.multiselect(
    "Select Drivers to Compare:",
    options=results["Abbreviation"].unique(),
    default=["VER", "LEC", "NOR"] if "VER" in results["Abbreviation"].unique() else results["Abbreviation"].unique()[:3]
)

if not selected_drivers:
    st.warning("Please select at least one driver.")
    st.stop()

filtered_laps = accurate_laps[accurate_laps["Driver"].isin(selected_drivers)]

# --- SECTION 1: RACE PACE COMPRASION ---
st.header("⏱️ Race Pace Comparison")
fig_pace = px.line(
    filtered_laps, 
    x="LapNumber", 
    y="LapTime", 
    color="Driver",
    hover_data=["Compound", "TyreLife", "Stint"],
    title="Lap Times over the Race (Lower is better)",
    labels={"LapNumber": "Lap", "LapTime": "Lap Time (Seconds)"}
)
fig_pace.update_yaxes(autorange="reversed") # Invert Y axis so faster laps are higher visually
st.plotly_chart(fig_pace, use_container_width=True)


# --- SECTION 2: TYRE STRATEGY ---
st.header("🟡 Tyre Strategy Overview")

# Define official F1 tyre colors
color_map = {
    "SOFT": "red",
    "MEDIUM": "yellow",
    "HARD": "white",
    "INTERMEDIATE": "green",
    "WET": "blue"
}

stints = laps[laps["Driver"].isin(selected_drivers)].groupby(["Driver", "Stint", "Compound"])["LapNumber"].agg(['min', 'max']).reset_index()
stints = stints.rename(columns={'min': 'StartLap', 'max': 'EndLap'})

fig_tyres = go.Figure()

for i, driver in enumerate(selected_drivers):
    driver_stints = stints[stints["Driver"] == driver]
    for _, row in driver_stints.iterrows():
        color = color_map.get(str(row["Compound"]).upper(), "gray")
        fig_tyres.add_trace(go.Bar(
            y=[driver],
            x=[row["EndLap"] - row["StartLap"] + 1],
            base=[row["StartLap"] - 1],
            orientation='h',
            name=row["Compound"],
            marker=dict(color=color, line=dict(width=1, color='black')),
            hovertemplate=f"Driver: {driver}<br>Compound: {row['Compound']}<br>Laps: {row['StartLap']} to {row['EndLap']}<extra></extra>"
        ))

fig_tyres.update_layout(
    barmode='stack',
    title="Driver Stints and Tyre Compounds",
    xaxis_title="Lap Number",
    yaxis_title="Driver",
    showlegend=False
)
st.plotly_chart(fig_tyres, use_container_width=True)

# --- SECTION 3: SECTOR ANALYSIS ---
st.header("🏁 Fastest Sectors Comparison")
fastest_sectors = filtered_laps.groupby("Driver")[["Sector1Time", "Sector2Time", "Sector3Time"]].min().reset_index()

col1, col2, col3 = st.columns(3)
with col1:
    st.subheader("Sector 1")
    fig_s1 = px.bar(fastest_sectors, x="Driver", y="Sector1Time", color="Driver", text_auto=".3f", title="Fastest S1 (Seconds)")
    fig_s1.update_yaxes(range=[fastest_sectors["Sector1Time"].min() * 0.95, fastest_sectors["Sector1Time"].max() * 1.05])
    st.plotly_chart(fig_s1, use_container_width=True)
with col2:
    st.subheader("Sector 2")
    fig_s2 = px.bar(fastest_sectors, x="Driver", y="Sector2Time", color="Driver", text_auto=".3f", title="Fastest S2 (Seconds)")
    fig_s2.update_yaxes(range=[fastest_sectors["Sector2Time"].min() * 0.95, fastest_sectors["Sector2Time"].max() * 1.05])
    st.plotly_chart(fig_s2, use_container_width=True)
with col3:
    st.subheader("Sector 3")
    fig_s3 = px.bar(fastest_sectors, x="Driver", y="Sector3Time", color="Driver", text_auto=".3f", title="Fastest S3 (Seconds)")
    fig_s3.update_yaxes(range=[fastest_sectors["Sector3Time"].min() * 0.95, fastest_sectors["Sector3Time"].max() * 1.05])
    st.plotly_chart(fig_s3, use_container_width=True)

# --- SECTION 4: DATA PREVIEW ---
st.header("📄 Database Explorer")
st.dataframe(filtered_laps[["Driver", "LapNumber", "LapTime", "Compound", "TyreLife", "Sector1Time", "Sector2Time", "Sector3Time"]])

st.markdown("---")
st.markdown("Built with **Streamlit** + **Plotly** + **FastF1** | AI Agent Demo")
