# -*- coding: utf-8 -*-

import streamlit as st
import pandas as pd
import plotly.express as px


def show_uncertainty():

    st.title("❓ Uncertainty Analysis")

    st.write("""
    Analisis keputusan di bawah ketidakpastian
    menggunakan metode Maximax, Maximin,
    Laplace, dan Minimax Regret.
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

    # =====================================
    # CALCULATIONS
    # =====================================

    maximax = payoff_df.max(axis=1)

    maximin = payoff_df.min(axis=1)

    laplace = payoff_df.mean(axis=1)

    regret = payoff_df.max() - payoff_df

    minimax = regret.max(axis=1)

    # =====================================
    # RESULT TABLE
    # =====================================

    result = pd.DataFrame({

        "Location": payoff_df.index,

        "Maximax": maximax.values,

        "Maximin": maximin.values,

        "Laplace": laplace.values,

        "Minimax Regret": minimax.values

    })

    st.subheader(
        "📋 Uncertainty Analysis Table"
    )

    st.dataframe(
        result,
        use_container_width=True
    )

    # =====================================
    # BEST RESULT
    # =====================================

    best_maximax = maximax.idxmax()

    best_maximin = maximin.idxmax()

    best_laplace = laplace.idxmax()

    best_minimax = minimax.idxmin()

    st.subheader(
        "🏆 Best Alternative by Method"
    )

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Maximax",
            best_maximax
        )

        st.metric(
            "Laplace",
            best_laplace
        )

    with col2:

        st.metric(
            "Maximin",
            best_maximin
        )

        st.metric(
            "Minimax Regret",
            best_minimax
        )

    # =====================================
    # MAXIMAX CHART
    # =====================================

    st.subheader(
        "🌟 Maximax Ranking"
    )

    maximax_df = pd.DataFrame({

        "Location": maximax.index,

        "Score": maximax.values

    })

    maximax_df = maximax_df.sort_values(
        by="Score",
        ascending=False
    )

    fig_maximax = px.bar(
        maximax_df,
        x="Location",
        y="Score",
        color="Score",
        color_continuous_scale="Brwnyl"
    )

    st.plotly_chart(
        fig_maximax,
        use_container_width=True
    )

    # =====================================
    # MAXIMIN CHART
    # =====================================

    st.subheader(
        "🛡️ Maximin Ranking"
    )

    maximin_df = pd.DataFrame({

        "Location": maximin.index,

        "Score": maximin.values

    })

    maximin_df = maximin_df.sort_values(
        by="Score",
        ascending=False
    )

    fig_maximin = px.bar(
        maximin_df,
        x="Location",
        y="Score",
        color="Score",
        color_continuous_scale="Brwnyl"
    )

    st.plotly_chart(
        fig_maximin,
        use_container_width=True
    )

    # =====================================
    # LAPLACE CHART
    # =====================================

    st.subheader(
        "⚖️ Laplace Ranking"
    )

    laplace_df = pd.DataFrame({

        "Location": laplace.index,

        "Score": laplace.values

    })

    laplace_df = laplace_df.sort_values(
        by="Score",
        ascending=False
    )

    fig_laplace = px.bar(
        laplace_df,
        x="Location",
        y="Score",
        color="Score",
        color_continuous_scale="Brwnyl"
    )

    st.plotly_chart(
        fig_laplace,
        use_container_width=True
    )

    # =====================================
    # MINIMAX CHART
    # =====================================

    st.subheader(
        "📉 Minimax Regret Ranking"
    )

    minimax_df = pd.DataFrame({

        "Location": minimax.index,

        "Score": minimax.values

    })

    minimax_df = minimax_df.sort_values(
        by="Score",
        ascending=True
    )

    fig_minimax = px.bar(
        minimax_df,
        x="Location",
        y="Score",
        color="Score",
        color_continuous_scale="Brwnyl"
    )

    st.plotly_chart(
        fig_minimax,
        use_container_width=True
    )

    # =====================================
    # VOTING RESULT
    # =====================================

    st.subheader(
        "🗳️ Method Voting"
    )

    votes = [

        best_maximax,
        best_maximin,
        best_laplace,
        best_minimax

    ]

    voting_df = (
        pd.Series(votes)
        .value_counts()
        .reset_index()
    )

    voting_df.columns = [
        "Location",
        "Votes"
    ]

    st.dataframe(
        voting_df,
        use_container_width=True
    )

    fig_vote = px.bar(
        voting_df,
        x="Location",
        y="Votes",
        color="Votes",
        color_continuous_scale="Brwnyl"
    )

    st.plotly_chart(
        fig_vote,
        use_container_width=True
    )

    # =====================================
    # FINAL RESULT
    # =====================================

    final_choice = voting_df.iloc[0]["Location"]

    confidence = round(
        (
            voting_df.iloc[0]["Votes"]
            / 4
        ) * 100,
        2
    )

    st.subheader(
        "🏆 Uncertainty Recommendation"
    )

    st.success(
        f"Lokasi terbaik adalah {final_choice}"
    )

    st.info(
        f"Tingkat konsensus metode: {confidence}%"
    )

    # =====================================
    # INTERPRETATION
    # =====================================

    st.subheader(
        "📝 Interpretation"
    )

    st.info(
        f"""
        Lokasi {final_choice}
        memperoleh dukungan terbanyak
        dari metode Maximax, Maximin,
        Laplace, dan Minimax Regret.

        Semakin tinggi tingkat konsensus,
        semakin kuat rekomendasi lokasi
        tersebut untuk dipilih.
        """
    )

    # =====================================
    # SAVE SESSION
    # =====================================

    st.session_state[
        "uncertainty_result"
    ] = final_choice

    st.session_state[
        "maximax_result"
    ] = best_maximax

    st.session_state[
        "maximin_result"
    ] = best_maximin

    st.session_state[
        "laplace_result"
    ] = best_laplace

    st.session_state[
        "minimax_result"
    ] = best_minimax
