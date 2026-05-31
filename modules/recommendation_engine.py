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

best_ev = st.session_state.get(
    "ev_result",
    ev.idxmax()
)

best_eol = st.session_state.get(
    "eol_result"
)

best_utility = st.session_state.get(
    "utility_result"
)

best_mc = st.session_state.get(
    "monte_carlo_result"
)

# =====================================
# VOTES FROM ALL DSS METHODS
# =====================================

votes = [

    best_maximax,
    best_maximin,
    best_laplace,
    best_minimax,

    best_ev,
    best_eol,

    best_utility,
    best_mc

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
        "Expected Value",
        "Expected Opportunity Loss",
        "Utility Function",
        "Monte Carlo"

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

ranking_df = vote_result.copy()

ranking_df = ranking_df.sort_values(
    by="Votes",
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
        "Votes",
        "Consensus (%)"
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
    y="Votes",
    color="Votes",
    color_continuous_scale="Brwnyl",
    title="Final DSS Ranking"
)

st.plotly_chart(
    fig_rank,
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
    dukungan dari {total_votes}
    metode DSS.

    Tingkat konsensus keputusan mencapai
    {confidence}%.

    Recommendation Engine menggabungkan
    hasil dari:

    • Expected Value (EV)

    • Expected Opportunity Loss (EOL)

    • Maximax

    • Maximin

    • Laplace

    • Minimax Regret

    • Utility Function

    • Monte Carlo Simulation

    Semakin tinggi jumlah vote dan
    konsensus, semakin kuat rekomendasi
    lokasi tersebut.
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
  
