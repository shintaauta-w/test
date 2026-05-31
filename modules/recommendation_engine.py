import streamlit as st
import pandas as pd
import numpy as np
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
    # DSS METHODS
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
    # METHOD RESULT TABLE
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

    vote_result["Consensus (%)"] = round(
        vote_result["Votes"]
        /
        len(votes)
        * 100,
        2
    )

    final_choice = vote_result.iloc[0][
        "Location"
    ]

    total_votes = vote_result.iloc[0][
        "Votes"
    ]

    confidence = vote_result.iloc[0][
        "Consensus (%)"
    ]

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
    # FINAL RANKING
    # =====================================

    st.subheader(
        "📊 Final Ranking"
    )

    ranking_df = pd.DataFrame({

        "Location":
        ev.index,

        "Final Score":
        np.round(
            ev.values,
            4
        )

    })

    ranking_df = ranking_df.sort_values(
        by="Final Score",
        ascending=False
    )

    ranking_df["Rank"] = range(
        1,
        len(ranking_df) + 1
    )

    ranking_df = ranking_df[
        [
            "Rank",
            "Location",
            "Final Score"
        ]
    ]

    st.dataframe(
        ranking_df,
        use_container_width=True
    )

    # =====================================
    # TOP 3 LOCATION
    # =====================================

    st.subheader(
        "🥇 Top 3 Locations"
    )

    if len(ranking_df) >= 3:

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "🥇 Rank 1",
                ranking_df.iloc[0]["Location"]
            )

        with col2:

            st.metric(
                "🥈 Rank 2",
                ranking_df.iloc[1]["Location"]
            )

        with col3:

            st.metric(
                "🥉 Rank 3",
                ranking_df.iloc[2]["Location"]
            )

    # =====================================
    # FINAL SCORE CHART
    # =====================================

    fig_rank = px.bar(
        ranking_df,
        x="Location",
        y="Final Score",
        color="Final Score",
        color_continuous_scale="Brwnyl",
        title="Location Ranking Score"
    )

    st.plotly_chart(
        fig_rank,
        use_container_width=True
    )

    # =====================================
    # SENSITIVITY ANALYSIS
    # =====================================

    st.subheader(
        "🔬 Sensitivity Analysis"
    )

    sensitivity = []

    for col in payoff_df.columns:

        modified = payoff_df.copy()

        modified[col] = (
            modified[col] * 1.1
        )

        score = modified.dot(weights)

        sensitivity.append({

            "Criteria":
            col,

            "Best Location":
            score.idxmax()

        })

    sensitivity_df = pd.DataFrame(
        sensitivity
    )

    st.dataframe(
        sensitivity_df,
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
            "Consensus",
            f"{confidence}%"
        )

    # =====================================
    # DECISION EXPLANATION
    # =====================================

    st.subheader(
        "📝 Decision Explanation"
    )

    st.info(
        f"""
        Lokasi {final_choice} dipilih sebagai
        alternatif terbaik karena memperoleh
        dukungan dari {total_votes} metode DSS.

        Tingkat konsensus keputusan mencapai
        {confidence}%.

        Hasil diperoleh dari kombinasi
        Expected Value (EV),
        Maximax,
        Maximin,
        Laplace,
        dan Minimax Regret.

        Sensitivity Analysis digunakan
        untuk melihat stabilitas keputusan
        apabila terjadi perubahan nilai
        pada kriteria tertentu.
        """
    )

    # =====================================
    # SAVE SESSION
    # =====================================

    st.session_state[
        "final_recommendation"
    ] = final_choice

    st.session_state[
        "ranking_df"
    ] = ranking_df
