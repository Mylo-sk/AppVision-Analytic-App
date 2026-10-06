# utils/styling.py
"""
Professional CSS styling for AppVision Analytics
Dark mode theme with modern, interactive components
"""

import streamlit as st
from .config import COLORS

def load_css():
    """
    Inject comprehensive CSS for a modern, professional dark-themed UI
    WITH FIXED SELECTBOX VISIBILITY
    """
    css = f"""
    <style>
    /* ========================================================================
       GOOGLE FONTS & ROOT VARIABLES
       ======================================================================== */
    
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    :root {{
        --primary: {COLORS['primary']};
        --secondary: {COLORS['secondary']};
        --accent: {COLORS['accent']};
        --success: {COLORS['success']};
        --warning: {COLORS['warning']};
        --error: {COLORS['error']};
        --bg: {COLORS['background']};
        --card-bg: {COLORS['card_bg']};
        --text-primary: {COLORS['text_primary']};
        --text-secondary: {COLORS['text_secondary']};
        --border: {COLORS['border']};
        --shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.3);
        --shadow-md: 0 4px 6px rgba(0, 0, 0, 0.4);
        --shadow-lg: 0 10px 25px rgba(0, 0, 0, 0.5);
        --shadow-xl: 0 20px 40px rgba(0, 0, 0, 0.6);
        --radius-sm: 6px;
        --radius-md: 10px;
        --radius-lg: 16px;
        --transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }}
    
    /* ========================================================================
       BASE STYLES
       ======================================================================== */
    
    * {{
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }}
    
    .main {{
        background: var(--bg);
        color: var(--text-primary);
    }}
    
    .main .block-container {{
        padding: 2rem 3rem;
        max-width: 1400px;
        margin: 0 auto;
    }}
    
    /* ========================================================================
       HEADER SECTION
       ======================================================================== */
    
    .app-header {{
        background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
        padding: 3rem 2rem;
        border-radius: var(--radius-lg);
        box-shadow: var(--shadow-xl);
        text-align: center;
        margin-bottom: 2.5rem;
        position: relative;
        overflow: hidden;
        animation: fadeInDown 0.8s ease-out;
    }}
    
    .app-header::before {{
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        animation: pulse 3s ease-in-out infinite;
    }}
    
    .app-title {{
        font-size: 3.5rem;
        font-weight: 800;
        color: white;
        margin: 0;
        text-shadow: 2px 4px 8px rgba(0,0,0,0.3);
        letter-spacing: -1px;
        position: relative;
        z-index: 1;
    }}
    
    .app-subtitle {{
        font-size: 1.25rem;
        color: rgba(255,255,255,0.9);
        margin-top: 0.75rem;
        font-weight: 400;
        position: relative;
        z-index: 1;
    }}
    
    /* ========================================================================
       NAVIGATION PILLS
       ======================================================================== */
    
    .nav-pills {{
        display: flex;
        gap: 1rem;
        justify-content: center;
        margin-bottom: 2rem;
        flex-wrap: wrap;
    }}
    
    .nav-pill {{
        background: var(--card-bg);
        color: var(--text-primary);
        padding: 0.75rem 1.5rem;
        border-radius: 50px;
        font-weight: 600;
        font-size: 1rem;
        cursor: pointer;
        transition: var(--transition);
        border: 2px solid transparent;
        box-shadow: var(--shadow-sm);
    }}
    
    .nav-pill:hover {{
        background: var(--secondary);
        transform: translateY(-2px);
        box-shadow: var(--shadow-md);
        border-color: var(--accent);
    }}
    
    .nav-pill.active {{
        background: var(--accent);
        color: white;
        box-shadow: var(--shadow-md);
    }}
    
    /* ========================================================================
       METRIC CARDS
       ======================================================================== */
    
    .metric-card {{
        background: linear-gradient(145deg, var(--card-bg), rgba(30, 58, 138, 0.1));
        padding: 1.75rem;
        border-radius: var(--radius-lg);
        text-align: center;
        box-shadow: var(--shadow-md);
        border: 1px solid var(--border);
        transition: var(--transition);
        position: relative;
        overflow: hidden;
    }}
    
    .metric-card::before {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, var(--secondary), var(--accent));
    }}
    
    .metric-card:hover {{
        transform: translateY(-5px) scale(1.02);
        box-shadow: var(--shadow-lg);
        border-color: var(--accent);
    }}
    
    .metric-value {{
        font-size: 2.5rem;
        font-weight: 800;
        color: var(--accent);
        margin: 0.5rem 0;
        text-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }}
    
    .metric-label {{
        font-size: 0.95rem;
        color: var(--text-secondary);
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }}
    
    /* ========================================================================
       FORM SECTIONS
       ======================================================================== */
    
    .form-container {{
        background: var(--card-bg);
        padding: 2.5rem;
        border-radius: var(--radius-lg);
        box-shadow: var(--shadow-lg);
        margin: 2rem 0;
        border: 1px solid var(--border);
        animation: fadeIn 0.6s ease-out;
    }}
    
    .form-section-header {{
        color: var(--secondary);
        font-weight: 700;
        font-size: 1.4rem;
        margin-bottom: 1.5rem;
        padding-bottom: 0.75rem;
        border-bottom: 3px solid var(--border);
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }}
    
    .form-section-header::before {{
        content: '';
        width: 4px;
        height: 24px;
        background: var(--accent);
        border-radius: 2px;
    }}
    
    /* ========================================================================
       INPUT STYLING (Unified Dark Theme)
       ======================================================================== */
    
    .stNumberInput > div > div > input,
    .stTextInput > div > div > input {{
        background-color: rgba(15, 23, 42, 0.8) !important;
        border: 2px solid var(--border) !important;
        border-radius: var(--radius-md) !important;
        color: var(--text-primary) !important;
        font-size: 1rem !important;
        padding: 0.75rem 1rem !important;
        transition: var(--transition) !important;
        font-weight: 500 !important;
    }}
    
    .stNumberInput > div > div > input:hover,
    .stTextInput > div > div > input:hover {{
        border-color: var(--secondary) !important;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.15) !important;
        transform: translateY(-1px) !important;
    }}
    
    .stNumberInput > div > div > input:focus,
    .stTextInput > div > div > input:focus {{
        border-color: var(--accent) !important;
        box-shadow: 0 0 0 4px rgba(16, 185, 129, 0.2) !important;
        outline: none !important;
    }}
    
    /* ========================================================================
       SELECTBOX STYLING - FIXED FOR VISIBILITY
       ======================================================================== */
    
    /* Main selectbox container */
    .stSelectbox > div > div {{
        background-color: rgba(15, 23, 42, 0.8) !important;
        border: 2px solid var(--border) !important;
        border-radius: var(--radius-md) !important;
        transition: var(--transition) !important;
    }}
    
    /* Selected value display - CRITICAL FIX */
    .stSelectbox > div > div > div {{
        color: #F1F5F9 !important;
        font-weight: 500 !important;
    }}
    
    /* Input field in selectbox */
    .stSelectbox input {{
        color: #F1F5F9 !important;
        background-color: transparent !important;
        caret-color: var(--accent) !important;
    }}
    
    /* Selectbox when typing */
    .stSelectbox [data-baseweb="input"] {{
        color: #F1F5F9 !important;
        background-color: transparent !important;
    }}
    
    /* Selected option container */
    .stSelectbox [data-baseweb="select"] > div {{
        color: #F1F5F9 !important;
    }}
    
    /* Text span inside selectbox */
    .stSelectbox [data-baseweb="select"] span {{
        color: #F1F5F9 !important;
    }}
    
    /* Button that shows selected value */
    .stSelectbox [role="button"] > div {{
        color: #F1F5F9 !important;
    }}
    
    /* Placeholder text */
    .stSelectbox [data-baseweb="input"]::placeholder {{
        color: var(--text-secondary) !important;
        opacity: 0.7 !important;
    }}
    
    /* Hover state */
    .stSelectbox > div > div:hover {{
        border-color: var(--secondary) !important;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.15) !important;
        transform: translateY(-1px) !important;
    }}
    
    /* Focus state */
    .stSelectbox > div > div:focus-within {{
        border-color: var(--accent) !important;
        box-shadow: 0 0 0 4px rgba(16, 185, 129, 0.2) !important;
        outline: none !important;
    }}
    
    /* Dropdown menu */
    div[role="listbox"] {{
        background-color: var(--card-bg) !important;
        border: 1px solid var(--border) !important;
        border-radius: var(--radius-md) !important;
        box-shadow: var(--shadow-lg) !important;
    }}
    
    /* Dropdown options */
    div[role="option"] {{
        color: var(--text-primary) !important;
        padding: 0.75rem 1rem !important;
        transition: var(--transition) !important;
    }}
    
    div[role="option"]:hover {{
        background-color: var(--secondary) !important;
        color: white !important;
    }}
    
    /* ========================================================================
       SLIDER STYLING
       ======================================================================== */
    
    .stSlider > div > div > div {{
        background: linear-gradient(90deg, var(--secondary), var(--accent)) !important;
        height: 8px !important;
        border-radius: 4px !important;
    }}
    
    .stSlider > div > div > div > div {{
        background: white !important;
        width: 24px !important;
        height: 24px !important;
        border-radius: 50% !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.4), 0 0 0 4px var(--secondary) !important;
        transition: var(--transition) !important;
    }}
    
    .stSlider > div > div > div > div:active {{
        cursor: grabbing !important;
    }}
    
    .stSlider > div > div > div > div:hover {{
        transform: scale(1.2) !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.5), 0 0 0 6px var(--accent) !important;
    }}
    
    /* ========================================================================
       RADIO BUTTONS
       ======================================================================== */
    
    .stRadio > div {{
        background: rgba(15, 23, 42, 0.4);
        padding: 1rem;
        border-radius: var(--radius-md);
        border: 2px solid var(--border);
        transition: var(--transition);
    }}
    
    .stRadio > div:hover {{
        border-color: var(--secondary);
        background: rgba(59, 130, 246, 0.1);
    }}
    
    .stRadio > div > label > div {{
        color: var(--text-primary) !important;
        font-weight: 500 !important;
    }}
    
    /* ========================================================================
       LABELS
       ======================================================================== */
    
    .stSelectbox label,
    .stSlider label,
    .stNumberInput label,
    .stTextInput label,
    .stRadio label {{
        font-weight: 600 !important;
        color: var(--text-primary) !important;
        font-size: 1rem !important;
        margin-bottom: 0.5rem !important;
        display: flex !important;
        align-items: center !important;
        gap: 0.5rem !important;
    }}
    
    /* ========================================================================
       BUTTONS
       ======================================================================== */
    
    .stButton > button {{
        background: linear-gradient(135deg, var(--secondary), var(--accent)) !important;
        color: white !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
        padding: 0.9rem 2.5rem !important;
        border-radius: 50px !important;
        border: none !important;
        box-shadow: var(--shadow-md) !important;
        transition: var(--transition) !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
    }}
    
    .stButton > button:hover {{
        transform: translateY(-3px) scale(1.03) !important;
        box-shadow: var(--shadow-xl) !important;
        background: linear-gradient(135deg, var(--accent), var(--secondary)) !important;
    }}
    
    .stButton > button:active {{
        transform: translateY(-1px) scale(0.98) !important;
    }}
    
    /* ========================================================================
       ALERTS & MESSAGES
       ======================================================================== */
    
    .stSuccess, .stInfo, .stWarning, .stError {{
        border-radius: var(--radius-md) !important;
        padding: 1rem 1.25rem !important;
        font-weight: 500 !important;
        box-shadow: var(--shadow-sm) !important;
        border-left: 4px solid !important;
    }}
    
    .stSuccess {{
        background: rgba(5, 150, 105, 0.15) !important;
        border-left-color: var(--success) !important;
        color: #6EE7B7 !important;
    }}
    
    .stInfo {{
        background: rgba(59, 130, 246, 0.15) !important;
        border-left-color: var(--secondary) !important;
        color: #93C5FD !important;
    }}
    
    .stWarning {{
        background: rgba(245, 158, 11, 0.15) !important;
        border-left-color: var(--warning) !important;
        color: #FCD34D !important;
    }}
    
    .stError {{
        background: rgba(239, 68, 68, 0.15) !important;
        border-left-color: var(--error) !important;
        color: #FCA5A5 !important;
    }}
    
    /* ========================================================================
       SIDEBAR
       ======================================================================== */
    
    .css-1d391kg, [data-testid="stSidebar"] {{
        background: var(--card-bg) !important;
        border-right: 1px solid var(--border) !important;
    }}
    
    .css-1d391kg .stProgress > div > div {{
        background: var(--secondary) !important;
    }}
    
    /* ========================================================================
       PROGRESS BARS
       ======================================================================== */
    
    .stProgress > div > div > div {{
        background: linear-gradient(90deg, var(--secondary), var(--accent)) !important;
        border-radius: 4px !important;
    }}
    
    /* ========================================================================
       ANIMATIONS
       ======================================================================== */
    
    @keyframes fadeIn {{
        from {{
            opacity: 0;
            transform: translateY(20px);
        }}
        to {{
            opacity: 1;
            transform: translateY(0);
        }}
    }}
    
    @keyframes fadeInDown {{
        from {{
            opacity: 0;
            transform: translateY(-30px);
        }}
        to {{
            opacity: 1;
            transform: translateY(0);
        }}
    }}
    
    @keyframes pulse {{
        0%, 100% {{
            opacity: 0.5;
        }}
        50% {{
            opacity: 0.8;
        }}
    }}
    
    .fade-in {{
        animation: fadeIn 0.6s ease-out;
    }}
    
    /* ========================================================================
       RESULT CARD
       ======================================================================== */
    
    .result-card {{
        background: linear-gradient(145deg, var(--card-bg), rgba(16, 185, 129, 0.1));
        padding: 2.5rem;
        border-radius: var(--radius-lg);
        box-shadow: var(--shadow-xl);
        border: 2px solid var(--accent);
        margin: 2rem 0;
        text-align: center;
        animation: fadeIn 0.8s ease-out;
    }}
    
    .result-title {{
        font-size: 2rem;
        font-weight: 800;
        color: var(--accent);
        margin-bottom: 1rem;
    }}
    
    .result-value {{
        font-size: 4rem;
        font-weight: 900;
        background: linear-gradient(135deg, var(--secondary), var(--accent));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 1rem 0;
    }}
    
    .result-description {{
        font-size: 1.1rem;
        color: var(--text-secondary);
        line-height: 1.6;
    }}
    
    /* ========================================================================
       DIVIDERS
       ======================================================================== */
    
    hr {{
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, var(--border), transparent);
        margin: 2rem 0;
    }}
    
    /* ========================================================================
       EXPANDER
       ======================================================================== */
    
    .streamlit-expanderHeader {{
        background: var(--card-bg) !important;
        border: 2px solid var(--border) !important;
        border-radius: var(--radius-md) !important;
        font-weight: 600 !important;
        color: var(--text-primary) !important;
    }}
    
    .streamlit-expanderHeader:hover {{
        border-color: var(--secondary) !important;
        background: rgba(59, 130, 246, 0.1) !important;
    }}
    
    /* ========================================================================
       TOOLTIPS
       ======================================================================== */
    
    [data-baseweb="tooltip"] {{
        background: var(--card-bg) !important;
        border: 1px solid var(--border) !important;
        border-radius: var(--radius-md) !important;
        box-shadow: var(--shadow-lg) !important;
        color: var(--text-primary) !important;
        padding: 0.75rem 1rem !important;
        font-size: 0.9rem !important;
    }}
    
    </style>
    """
    
    st.markdown(css, unsafe_allow_html=True)


def create_header(title, subtitle):
    """
    Create professional animated header
    """
    header_html = f"""
    <div class="app-header fade-in">
        <div class="app-title">{title}</div>
        <div class="app-subtitle">{subtitle}</div>
    </div>
    """
    st.markdown(header_html, unsafe_allow_html=True)


def create_metric_card(icon, value, label):
    """
    Create a single metric card
    """
    card_html = f"""
    <div class="metric-card fade-in">
        <div style="font-size:2.5rem;">{icon}</div>
        <div class="metric-value">{value}</div>
        <div class="metric-label">{label}</div>
    </div>
    """
    return card_html


def create_section_header(text, icon=""):
    """
    Create styled section header
    """
    header_html = f"""
    <div class="form-section-header">
        {icon} {text}
    </div>
    """
    st.markdown(header_html, unsafe_allow_html=True)
