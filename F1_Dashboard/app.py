import streamlit as st
from utils.styling import apply_f1_theme

# Page Configuration
st.set_page_config(
    page_title="F1 Analytics Dashboard",
    page_icon="🏎️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Apply global styling
apply_f1_theme()

# Sidebar Navigation
st.sidebar.title("🏎️ F1 Analytics")
page = st.sidebar.radio(
    "Navigation", 
    ["Season View", "Grand Prix View", "Race View"]
)

# Routing
if page == "Season View":
    from views import season
    season.render()
elif page == "Grand Prix View":
    from views import grand_prix
    grand_prix.render()
elif page == "Race View":
    from views import race
    race.render()

st.sidebar.markdown("---")
st.sidebar.caption("Data provided by FastF1 & Ergast")
