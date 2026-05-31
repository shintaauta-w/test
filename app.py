import streamlit as st

from config import APP_TITLE, PAGE_ICON

from ui.styles import load_css
from ui.sidebar import sidebar_menu

from modules.dashboard import show_dashboard
from modules.data_driven import show_data_driven
from modules.criteria_weight import show_criteria_weight
from modules.payoff_table import show_payoff_table
from modules.ev_eol import show_ev_eol
from modules.uncertainty import show_uncertainty
from modules.distribution import show_distribution
from modules.utility import show_utility
from modules.monte_carlo import show_monte_carlo
from modules.recommendation_engine import show_recommendation

st.set_page_config(
    page_title=APP_TITLE,
    page_icon=PAGE_ICON,
    layout="wide"
)

load_css()

menu = sidebar_menu()

if menu == "🏠 Dashboard":

    show_dashboard()

elif menu == "📊 Data-Driven DSS":

    show_data_driven()

elif menu == "⚖️ Criteria Weight":

    show_criteria_weight()

elif menu == "📋 Payoff Table":

    show_payoff_table()

elif menu == "🎲 EV & EOL":

    show_ev_eol()

elif menu == "❓ Uncertainty":

    show_uncertainty()

elif menu == "📈 Distribution":

    show_distribution()

elif menu == "⚖️ Utility Function":

    show_utility()

elif menu == "🎰 Monte Carlo":

    show_monte_carlo()

elif menu == "🏆 Recommendation":

    show_recommendation()

