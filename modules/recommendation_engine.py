# -*- coding: utf-8 -*-

import streamlit as st
import pandas as pd
import plotly.express as px


def show_recommendation():

    st.title("🏆 Recommendation Engine")

    st.write("""
    Modul ini menggabungkan seluruh metode DSS
    untuk menghasilkan rekomendasi lokasi usaha terbaik.
    """)

    # =====================================
    # VALIDATION
    # =====================================

    if (
        "payoff_df" not in st.session_state
        or st.session_state["payoff_df"] is None
    ):

        st.warning(
            "⚠️ Generate payoff matrix terlebih dahulu."
        )

        return

    if (
        "criteria_weights" not in st.session_state
    ):

        st.warning(
            "⚠️ Tentukan bobot kriteria terlebih dahulu."
        )

        return

    # =====================================
    # LOAD MATRIX
    # =====================================

    if (
        "weighted_payoff_df" in st.session_state
        and st.session_state["weighted_payoff_df"] is not None
    ):

        payoff_df = st.session_state[
            "weighted_payoff_df"
        ]

    else:

        payoff_df = st.session_state[
            "payoff_df"
        ]

    weights = list(
        st.session_state[
            "criteria_weights"
        ].values()
    )

    # =====================================
    # CALCULATE METHODS
    # =====================================

    maximax = payoff_df.max(axis=1)

    maximin = payoff_df.min(axis=1)

    laplace = payoff_df.mean(axis=1)

    regret = payoff_df.max() - payoff_df

    minimax = regret.max(axis=1)

    ev = payoff_df.dot(weights)

    # =====================================
    # BEST RESULT EACH METHOD
    # =====================================

    best_maximax = maximax.idxmax()

    best_maximin = maximin.idxmax()

    best_laplace = laplace.idxmax()

    best_minimax = minimax.idxmin()

    best_ev = ev.idxmax()

    votes = [

        best_maximax,
        best_maximin,
        best_laplace,
        best_minimax,
        best_ev

    ]

    # =====================================
    # VOTING RESULT
    # =====================================

    vote_result = (
        pd.Series(votes)
        .value_counts()
        .reset_index()
    )

    vote_result.columns = [
        "Location",
        "Votes"
    ]

    final_choice = vote_result.iloc[0]["Location"]

    total_votes = vote_result.iloc[0]["Votes"]

    confidence = round(
        (total_votes / len(votes)) * 100,
        2
    )

    # =====================================
    # METHOD TABLE
    # =====================================

    st.subheader(
        "📋 Recommendation by Method"
    )

    method_df = pd.DataFrame({

        "Method": [

            "Maximax",
            "Maximin",
            "Laplace",
            "Minimax Regret",
            "Expected Value"

        ],

        "Recommendation": votes

    })

    st.dataframe(
        method_df,
        use_container_width=True
    )

    # =====================================
    # VOTING TABLE
    # =====================================

    st.subheader(
        "🗳️ Voting Result"
    )

    st.dataframe(
        vote_result,
        use_container_width=True
    )

    # =====================================
    # VOTING CHART
    # =====================================

    fig_vote = px.bar(
        vote_result,
        x="Location",
        y="Votes",
        color="Votes",
        color_continuous_scale="Brwnyl",
        title="Voting Distribution"
    )

    st.plotly_chart(
        fig_vote,
        use_container_width=True
    )

    # =====================================
    # FINAL RESULT
    # =====================================

    st.subheader(
        "🏆 Final Recommendation"
    )

    st.success(
        f"Lokasi terbaik adalah {final_choice}"
    )

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Votes",
            total_votes
        )

    with col2:

        st.metric(
            "Confidence",
            f"{confidence}%"
        )

    # =====================================
    # EV RANKING
    # =====================================

    st.subheader(
        "📊 Expected Value Ranking"
    )

    ranking_df = pd.DataFrame({

        "Location": ev.index,

        "EV Score": ev.values

    })

    ranking_df = ranking_df.sort_values(
        by="EV Score",
        ascending=False
    )

    ranking_df.reset_index(
        drop=True,
        inplace=True
    )

    ranking_df.index += 1

    st.dataframe(
        ranking_df,
        use_container_width=True
    )

    # =====================================
    # EXPLANATION
    # =====================================

    st.subheader(
        "📝 Decision Explanation"
    )

    st.info(
        f"""
        Lokasi {final_choice} dipilih karena memperoleh
        dukungan dari {total_votes} metode DSS
        dengan tingkat konsensus sebesar
        {confidence}%.
        
        Hasil ini diperoleh dari kombinasi
        metode Expected Value (EV),
        Maximax, Maximin,
        Laplace, dan Minimax Regret.
        """
    )

    # =====================================
    # STORE SESSION
    # =====================================

    st.session_state[
        "final_recommendation"
    ] = final_choice
