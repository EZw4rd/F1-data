import streamlit as st

def apply_f1_theme():
    """
    Applies custom CSS to enforce the F1 Dark Mode aesthetic (#15151E).
    """
    custom_css = """
    <style>
        /* F1 Dark Theme Background */
        .stApp {
            background-color: #15151E;
            color: #FFFFFF;
        }
        
        /* Sidebar styling */
        [data-testid="stSidebar"] {
            background-color: #111118;
        }

        /* Monospace fonts for numbers/tables */
        .dataframe {
            font-family: 'Courier New', Courier, monospace !important;
        }
        
        /* Hide row indices by default if needed */
        .row_heading.level0 {display:none}
        .blank {display:none}
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)

# Centralized Color Maps
TEAM_COLORS = {
    'Red Bull Racing': '#3671C6',
    'Mercedes': '#27F4D2',
    'Ferrari': '#E80020',
    'McLaren': '#FF8000',
    'Aston Martin': '#229971',
    'Alpine': '#FF87BC',
    'Williams': '#64C4FF',
    'RB': '#6692FF',
    'Kick Sauber': '#52E252',
    'Haas F1 Team': '#B6BABD',
}

# We can use FastF1's built in driver colors to ensure teammates have distinct coloring
import fastf1.plotting
fastf1.plotting.setup_mpl(misc_mpl_mods=False, color_scheme='fastf1')

def get_driver_color(driver_code, team_name):
    """
    Returns a distinct hex color for a driver. Tries FastF1 native first, falls back to Team Color.
    """
    try:
        color = fastf1.plotting.driver_color(driver_code)
        if color:
            return color
    except Exception:
        pass
    
    # Fallback if fastf1 doesn't know the driver
    return TEAM_COLORS.get(team_name, '#FFFFFF')

TYRE_COLORS = {
    'SOFT': '#FF3333',
    'MEDIUM': '#EAEA00',
    'HARD': '#FFFFFF',
    'INTERMEDIATE': '#39B54A',
    'WET': '#00AEEF',
    'UNKNOWN': '#808080'
}
