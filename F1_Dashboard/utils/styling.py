import streamlit as st
import plotly.graph_objects as go

def apply_f1_theme():
    """
    Applies custom CSS to enforce the F1 premium aesthetic.
    """
    custom_css = """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&family=Fira+Code:wght@400;700&display=swap');
        
        /* Global Font Override */
        html, body, [class*="css"] {
            font-family: 'Outfit', sans-serif !important;
        }

        /* F1 Dark Theme Background */
        .stApp {
            background-color: #15151E;
            color: #FFFFFF;
        }
        
        /* Sidebar styling */
        [data-testid="stSidebar"] {
            background-color: #111115 !important;
            border-right: 1px solid #2A2A35;
        }

        /* Hide Streamlit Top Menu & Footer */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {background-color: transparent !important;}

        /* Monospace fonts for numbers/tables */
        .dataframe {
            font-family: 'Fira Code', monospace !important;
        }
        
        /* Custom F1 Cards for Metrics / Insights */
        .f1-card {
            background: rgba(42, 42, 53, 0.4);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 4px 30px rgba(0, 0, 0, 0.5);
            backdrop-filter: blur(8px);
            -webkit-backdrop-filter: blur(8px);
            transition: transform 0.2s ease, border 0.2s ease;
        }
        
        .f1-card:hover {
            transform: translateY(-2px);
            border: 1px solid #E80020; /* F1 Red glow */
        }
        
        .f1-card h3 {
            margin-top: 0;
            color: #FFFFFF;
            font-weight: 600;
        }
        
        .f1-stat-val {
            font-size: 2rem;
            font-weight: 800;
            color: #E80020;
            font-family: 'Fira Code', monospace;
            margin-bottom: 5px;
        }
        
        .f1-stat-label {
            font-size: 0.9rem;
            color: #B6BABD;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        /* Customize Streamlit Tabs */
        .stTabs [data-baseweb="tab-list"] {
            gap: 24px;
        }
        .stTabs [data-baseweb="tab"] {
            height: 50px;
            white-space: pre-wrap;
            background-color: transparent;
            border-radius: 4px 4px 0px 0px;
            gap: 1px;
            padding-top: 10px;
            padding-bottom: 10px;
            color: #B6BABD;
        }
        .stTabs [aria-selected="true"] {
            color: #FFFFFF !important;
            border-bottom-color: #E80020 !important;
            font-weight: 800 !important;
        }
        
        /* Dataframes */
        [data-testid="stDataFrame"] {
            border-radius: 8px;
            overflow: hidden;
            border: 1px solid #2A2A35;
        }
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)

def apply_premium_chart_layout(fig, title=None, height=600):
    """
    Applies a premium, transparent, broadcast-quality layout to a Plotly figure.
    """
    fig.update_layout(
        title=dict(
            text=title if title else "",
            font=dict(family="Outfit", size=24, color="#FFFFFF"),
            x=0.01,
            y=0.98
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Outfit', color='#B6BABD', size=13),
        height=height,
        margin=dict(t=50, l=40, r=20, b=40),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            bgcolor='rgba(0,0,0,0.5)',
            bordercolor='rgba(255,255,255,0.1)',
            borderwidth=1,
            font=dict(color="#FFFFFF")
        ),
        hoverlabel=dict(
            bgcolor="rgba(21, 21, 30, 0.9)",
            font_size=14,
            font_family="Outfit",
            bordercolor="#E80020"
        ),
        xaxis=dict(
            showgrid=True,
            gridcolor='rgba(255,255,255,0.05)',
            gridwidth=1,
            zeroline=False,
            color="#FFFFFF"
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='rgba(255,255,255,0.05)',
            gridwidth=1,
            zeroline=False,
            color="#FFFFFF"
        )
    )
    return fig


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

# FastF1 plotting is imported lazily to avoid module-level failures
_fastf1_plotting_initialized = False

def get_driver_color(driver_code, team_name):
    """
    Returns a distinct hex color for a driver. Tries FastF1 native first, falls back to Team Color.
    """
    global _fastf1_plotting_initialized
    try:
        import fastf1.plotting
        if not _fastf1_plotting_initialized:
            fastf1.plotting.setup_mpl(misc_mpl_mods=False, color_scheme='fastf1')
            _fastf1_plotting_initialized = True
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
