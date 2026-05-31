import streamlit as st
import pandas as pd

def show_payoff_table():

    st.title("📋 Payoff Table")

    st.write("""
    Modul ini menampilkan payoff matrix yang akan digunakan
    pada seluruh metode pengambilan keputusan.
    """)

    # =====================================
    # LOAD MATRIX
    # =====================================

    matrix_type = ""

    if (
        "weighted_payoff_df" in st.session_state
        and st.session_state["weighted_payoff_df"] is not None
    ):

        payoff_df = st.session_state[
            "weighted_payoff_df"
        ]

        matrix_type = "Weighted Matrix"

    elif (
        "payoff_df" in st.session_state
        and st.session_state["payoff_df"] is not None
    ):

        payoff_df = st.session_state[
            "payoff_df"
        ]

        matrix_type = "Original Matrix"

    else:

        st.warning(
            "⚠️ No payoff matrix available."
        )

        return

    # =====================================
    # MATRIX STATUS
    # =====================================

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Alternatives",
            payoff_df.shape[0]
        )

    with col2:

        st.metric(
            "Criteria",
            payoff_df.shape[1]
        )

    with col3:

        st.metric(
            "Matrix Type",
            matrix_type
        )

    # =====================================
    # DISPLAY MATRIX
    # =====================================

    st.subheader(
        "📊 Payoff Matrix"
    )

    st.dataframe(
        payoff_df,
        use_container_width=True
    )

    # =====================================
    # SUMMARY STATISTICS
    # =====================================

    st.subheader(
        "📈 Summary Statistics"
    )

    st.dataframe(
        payoff_df.describe(),
        use_container_width=True
    )

    # =====================================
    # BEST VALUE PER CRITERIA
    # =====================================

    st.subheader(
        "🏆 Best Value for Each Criterion"
    )

    best_df = pd.DataFrame({

        "Criterion": payoff_df.columns,

        "Best Alternative": [
            payoff_df[col].idxmax()
            for col in payoff_df.columns
        ],

        "Best Score": [
            round(
                payoff_df[col].max(),
                4
            )
            for col in payoff_df.columns
        ]

    })

    st.dataframe(
        best_df,
        use_container_width=True
    )

    # =====================================
    # RANKING BASED ON TOTAL SCORE
    # =====================================

    st.subheader(
        "🥇 Overall Ranking"
    )

    ranking_df = pd.DataFrame({

        "Location": payoff_df.index,

        "Total Score": payoff_df.sum(axis=1)

    })

    ranking_df = ranking_df.sort_values(
        by="Total Score",
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
    # STORE TOP LOCATION
    # =====================================

    st.session_state[
        "payoff_best_location"
    ] = ranking_df.iloc[0]["Location"]

    st.success(
        f"🏆 Current Best Location : {ranking_df.iloc[0]['Location']}"
    )
