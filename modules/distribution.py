# -*- coding: utf-8 -*-

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

def show_distribution():

    st.title("📈 Distribution Analysis")

    # =====================================
    # CHECK MATRIX
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
    # CALCULATE DISTRIBUTION
    # =====================================

    mean_score = payoff_df.mean(axis=1)

    std_score = payoff_df.std(axis=1)

    cv_score = (
        std_score /
        (mean_score + 1e-9)
    )

    result_df = pd.DataFrame({

        "Location":
        payoff_df.index,

        "Mean Score":
        np.round(
            mean_score.values,
            4
        ),

        "Std Deviation":
        np.round(
            std_score.values,
            4
        ),

        "CV":
        np.round(
            cv_score.values,
            4
        )

    })

    result_df = result_df.sort_values(
        by="Mean Score",
        ascending=False
    )

    # =====================================
    # TABLE
    # =====================================

    st.subheader(
        "📋 Risk & Return Table"
    )

    st.dataframe(
        result_df,
        use_container_width=True
    )

    # =====================================
    # BEST RETURN
    # =====================================

    best_return = mean_score.idxmax()

    safest_location = cv_score.idxmin()

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "🏆 Highest Return",
            best_return
        )

    with col2:

        st.metric(
            "🛡️ Lowest Risk",
            safest_location
        )

    # =====================================
    # RISK RETURN SCATTER
    # =====================================

    st.subheader(
        "📊 Risk vs Return"
    )

    scatter_df = pd.DataFrame({

        "Location":
        payoff_df.index,

        "Return":
        mean_score.values,

        "Risk":
        cv_score.values

    })

    fig = px.scatter(

        scatter_df,

        x="Risk",

        y="Return",

        text="Location",

        size="Return",

        color="Return",

        color_continuous_scale="Brwnyl"

    )

    fig.update_traces(
        textposition="top center"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # =====================================
    # INTERPRETATION
    # =====================================

    st.subheader(
        "📝 Interpretation"
    )

    st.info(
        f"""
        Best Return Location:
        {best_return}

        Lowest Risk Location:
        {safest_location}

        Return diukur menggunakan
        rata-rata payoff.

        Risk diukur menggunakan
        Coefficient of Variation (CV).
        Semakin kecil CV maka
        semakin stabil lokasi tersebut.
        """
    )

    # =====================================
    # SAVE RESULT
    # =====================================

    st.session_state[
        "distribution_result"
    ] = result_df

    st.success(
        "✅ Distribution analysis completed"
    )
