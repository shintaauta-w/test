# -*- coding: utf-8 -*-

import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px

def show_utility():

    st.title("⚖️ Utility Function Analysis")

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
    # RISK PREFERENCE
    # =====================================

    risk = st.selectbox(
        "Risk Preference",
        [
            "Risk Averse",
            "Risk Neutral",
            "Risk Seeking"
        ]
    )

    # =====================================
    # UTILITY CALCULATION
    # =====================================

    utility_scores = {}

    for location in payoff_df.index:

        values = payoff_df.loc[
            location
        ].values

        if risk == "Risk Averse":

            utility_values = np.sqrt(
                values + 1
            )

        elif risk == "Risk Neutral":

            utility_values = values

        else:

            utility_values = (
                values + 1
            ) ** 2

        utility_scores[
            location
        ] = np.mean(
            utility_values
        )

    utility_df = pd.DataFrame({

        "Location":
        list(
            utility_scores.keys()
        ),

        "Expected Utility":
        list(
            utility_scores.values()
        )

    })

    utility_df = utility_df.sort_values(
        by="Expected Utility",
        ascending=False
    )

    # =====================================
    # DISPLAY TABLE
    # =====================================

    st.subheader(
        "📋 Utility Ranking"
    )

    st.dataframe(
        utility_df,
        use_container_width=True
    )

    # =====================================
    # BAR CHART
    # =====================================

    fig = px.bar(
        utility_df,
        x="Location",
        y="Expected Utility",
        color="Expected Utility",
        color_continuous_scale="Brwnyl"
    )

    fig.update_layout(
        title=
        "Utility Comparison Across Locations"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # =====================================
    # BEST LOCATION
    # =====================================

    best_location = utility_df.iloc[
        0
    ]["Location"]

    best_score = utility_df.iloc[
        0
    ]["Expected Utility"]

    st.success(
        f"🏆 Best Utility Location : {best_location}"
    )

    st.info(
        f"Expected Utility Score = {round(best_score,4)}"
    )

    # =====================================
    # SAVE RESULT
    # =====================================

    st.session_state[
        "utility_result"
    ] = best_location
