import streamlit as st
from config import COLORS

def load_css():

    st.markdown(
        f"""
        <style>

        /* =====================================
        MAIN APP
        ===================================== */

        .main {{
            background-color: {COLORS['background']};
        }}

        .block-container {{
            padding-top: 2rem;
            padding-bottom: 2rem;
        }}

        /* =====================================
        HEADINGS
        ===================================== */

        h1, h2, h3, h4, h5, h6 {{
            color: {COLORS['primary']} !important;
            font-weight: 700;
        }}

        p, div, span, label {{
            color: {COLORS['text']} !important;
        }}

        /* =====================================
        SIDEBAR
        ===================================== */

        [data-testid="stSidebar"] {{
            background-color: {COLORS['secondary']};
        }}

        [data-testid="stSidebar"] * {{
            color: white !important;
        }}

        [data-testid="stSidebar"] hr {{
            border-color: rgba(255,255,255,0.3);
        }}

        /* =====================================
        BUTTON
        ===================================== */

        .stButton > button {{

            background-color:
            {COLORS['primary']} !important;

            color: white !important;

            border-radius: 12px;

            border: none;

            font-weight: bold;

            width: 100%;

            height: 50px;

            transition: 0.3s;
        }}

        .stButton > button:hover {{

            transform: scale(1.02);

            opacity: 0.9;
        }}

        /* =====================================
        METRIC CARD
        ===================================== */

        [data-testid="metric-container"] {{

            background-color: white;

            border-radius: 15px;

            padding: 15px;

            box-shadow:
            0 2px 10px rgba(0,0,0,0.08);

            border-left:
            5px solid {COLORS['primary']};
        }}

        /* =====================================
        DATAFRAME
        ===================================== */

        .stDataFrame {{

            border-radius: 15px;

            overflow: hidden;

            border: 1px solid #E5E5E5;
        }}

        /* =====================================
        SUCCESS BOX
        ===================================== */

        div[data-baseweb="notification"] {{

            border-radius: 12px;
        }}

        /* =====================================
        SELECTBOX
        ===================================== */

        .stSelectbox > div > div {{

            border-radius: 10px;
        }}

        /* =====================================
        SLIDER
        ===================================== */

        .stSlider {{

            padding-top: 10px;
        }}

        /* =====================================
        INFO CARD
        ===================================== */

        .custom-card {{

            background-color: white;

            padding: 20px;

            border-radius: 15px;

            box-shadow:
            0 2px 10px rgba(0,0,0,0.08);

            margin-bottom: 15px;
        }}

        /* =====================================
        TABLE HEADER
        ===================================== */

        thead tr th {{

            background-color:
            {COLORS['primary']} !important;

            color: white !important;
        }}

        /* =====================================
        FOOTER HIDE
        ===================================== */

        footer {{
            visibility: hidden;
        }}

        #MainMenu {{
            visibility: hidden;
        }}

        </style>
        """,
        unsafe_allow_html=True
    )
