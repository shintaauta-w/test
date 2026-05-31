import streamlit as st
import pandas as pd
import plotly.express as px


def show_criteria_weight():

    st.title("⚖️ Criteria Weight")

    st.write("""
    Modul ini digunakan untuk menentukan bobot setiap kriteria
    dan menghasilkan Weighted Payoff Matrix yang akan digunakan
    pada seluruh analisis DSS berikutnya.
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

    payoff_df = st.session_state["payoff_df"]

    # =====================================
    # WEIGHT INPUT
    # =====================================

    st.subheader(
        "🎯 Set Criteria Weights"
    )

    weights = {}

    total_weight = 0

    default_weight = round(
        1 / len(payoff_df.columns),
        2
    )

    for col in payoff_df.columns:

        weight = st.slider(
            f"{col}",
            min_value=0.0,
            max_value=1.0,
            value=float(default_weight),
            step=0.01,
            key=f"weight_{col}"
        )

        weights[col] = weight

        total_weight += weight

    # =====================================
    # TOTAL WEIGHT
    # =====================================

    st.info(
        f"Total Weight = {round(total_weight,2)}"
    )

    progress = min(
        total_weight,
        1.0
    )

    st.progress(progress)

    if round(total_weight,2) != 1.0:

        st.error(
            "⚠️ Total bobot harus sama dengan 1.00"
        )

        return

    # =====================================
    # WEIGHT VISUALIZATION
    # =====================================

    weight_df = pd.DataFrame({

        "Criteria": list(weights.keys()),

        "Weight": list(weights.values())

    })

    fig_weight = px.pie(
        weight_df,
        names="Criteria",
        values="Weight",
        title="Criteria Weight Distribution"
    )

    st.plotly_chart(
        fig_weight,
        use_container_width=True
    )

    # =====================================
    # CRITERIA TYPE
    # =====================================

    st.subheader(
        "⚖️ Criteria Type"
    )

    criteria_type = {}

    for col in payoff_df.columns:

        criteria_type[col] = st.selectbox(
            f"{col} Type",
            [
                "Benefit",
                "Cost"
            ],
            key=f"type_{col}"
        )

    # =====================================
    # NORMALIZATION
    # =====================================

    normalized_df = payoff_df.copy()

    for col in normalized_df.columns:

        max_val = normalized_df[col].max()
        min_val = normalized_df[col].min()

        if max_val == min_val:

            normalized_df[col] = 1

        else:

            if criteria_type[col] == "Benefit":

                normalized_df[col] = (
                    normalized_df[col]
                    /
                    max_val
                )

            else:

                normalized_df[col] = (
                    min_val
                    /
                    normalized_df[col]
                )

    # =====================================
    # WEIGHTED MATRIX
    # =====================================

    weighted_df = normalized_df.copy()

    for col in weighted_df.columns:

        weighted_df[col] = (
            weighted_df[col]
            * weights[col]
        )

    # =====================================
    # SUMMARY
    # =====================================

    st.subheader(
        "📋 Criteria Configuration"
    )

    config_df = pd.DataFrame({

        "Criteria": payoff_df.columns,

        "Weight": [
            weights[c]
            for c in payoff_df.columns
        ],

        "Type": [
            criteria_type[c]
            for c in payoff_df.columns
        ]

    })

    st.dataframe(
        config_df,
        use_container_width=True
    )

    # =====================================
    # WEIGHTED MATRIX
    # =====================================

    st.subheader(
        "📊 Weighted Payoff Matrix"
    )

    st.dataframe(
        weighted_df,
        use_container_width=True
    )

    # =====================================
    # LOCATION SCORE
    # =====================================

    total_score = weighted_df.sum(axis=1)

    ranking_df = pd.DataFrame({

        "Location": total_score.index,

        "Total Score": total_score.values

    })

    ranking_df = ranking_df.sort_values(
        by="Total Score",
        ascending=False
    )

    st.subheader(
        "🏆 Preliminary Ranking"
    )

    st.dataframe(
        ranking_df,
        use_container_width=True
    )

    # =====================================
    # STORE SESSION
    # =====================================

    st.session_state[
        "criteria_weights"
    ] = weights

    st.session_state[
        "criteria_type"
    ] = criteria_type

    st.session_state[
        "weighted_payoff_df"
    ] = weighted_df

    st.success(
        "✅ Weighted Matrix berhasil disimpan."
    )
