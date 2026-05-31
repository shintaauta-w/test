# -*- coding: utf-8 -*-
"""monte_carlo.py"""

import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px

def show_monte_carlo():

    st.title("🎰 Monte Carlo Simulation")

    # =====================================
    # CHECK DATA
    # =====================================

    if (
        "weighted_payoff_df" not in st.session_state
        or st.session_state["weighted_payoff_df"] is None
    ):

        st.warning(
            "⚠️ Please generate weighted payoff matrix first."
        )

        return

    payoff_df = st.session_state[
        "weighted_payoff_df"
    ]

    # =====================================
    # NUMBER OF SIMULATION
    # =====================================

    simulations = st.slider(
        "Number of Simulations",
        100,
        10000,
        5000
    )

    # =====================================
    # MONTE CARLO PROCESS
    # =====================================

    results = []

    for location in payoff_df.index:

        values = payoff_df.loc[
            location
        ].values

        simulated = np.random.normal(
            np.mean(values),
            np.std(values),
            simulations
        )

        results.append({

            "Location":
            location,

            "Expected Profit":
            np.mean(simulated),

            "Risk (Std)":
            np.std(simulated),

            "Maximum":
            np.max(simulated),

            "Minimum":
            np.min(simulated)

        })

    result_df = pd.DataFrame(
        results
    )

    result_df = result_df.sort_values(
        by="Expected Profit",
        ascending=False
    )

    # =====================================
    # RESULT TABLE
    # =====================================

    st.subheader(
        "📋 Monte Carlo Ranking"
    )

    st.dataframe(
        result_df,
        use_container_width=True
    )

    # =====================================
    # BEST RESULT
    # =====================================

    best_location = result_df.iloc[
        0
    ]["Location"]

    best_profit = result_df.iloc[
        0
    ]["Expected Profit"]

    # =====================================
    # METRICS
    # =====================================

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Best Location",
            best_location
        )

    with col2:

        st.metric(
            "Expected Profit",
            round(best_profit,4)
        )

    # =====================================
    # BAR CHART
    # =====================================

    fig = px.bar(
        result_df,
        x="Location",
        y="Expected Profit",
        color="Expected Profit",
        color_continuous_scale="Brwnyl",
        title=
        "Expected Profit by Location"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # =====================================
    # RISK VISUALIZATION
    # =====================================

    fig_risk = px.bar(
        result_df,
        x="Location",
        y="Risk (Std)",
        color="Risk (Std)",
        color_continuous_scale="Reds",
        title=
        "Risk Comparison Across Locations"
    )

    st.plotly_chart(
        fig_risk,
        use_container_width=True
    )

    # =====================================
    # SAVE RESULT
    # =====================================

    st.session_state[
        "monte_carlo_result"
    ] = best_location

    # =====================================
    # FINAL RESULT
    # =====================================

    st.success(
        f"🏆 Best Monte Carlo Location : {best_location}"
    )

    st.info(
        f"Expected Profit = {round(best_profit,4)}"
    )
