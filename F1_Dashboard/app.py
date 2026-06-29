import streamlit as st
from streamlit_option_menu import option_menu
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
with st.sidebar:
    st.markdown("<h1 style='text-align: center; color: white;'>🏎️ F1 Analytics</h1>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    page = option_menu(
        menu_title=None,  # Hide the default title
        options=["Season View", "Grand Prix View", "Race View"],
        icons=["calendar3", "map-fill", "speedometer2"],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "transparent"},
            "icon": {"color": "#E80020", "font-size": "18px"}, 
            "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#2A2A35"},
            "nav-link-selected": {"background-color": "#E80020", "color": "white", "font-weight": "bold"},
        }
    )

    st.markdown("---")
    st.markdown("<br>" * 10, unsafe_allow_html=True) # push to bottom
    
    if st.button("🧹 Clear Data Cache", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

    st.caption("Data provided by FastF1 & Ergast")

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

