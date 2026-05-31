import streamlit as st
import pandas as pd


def sidebar_menu():

    # =====================================
    # TITLE
    # =====================================

    st.sidebar.title(
        "🤎 Business Location DSS"
    )

    st.sidebar.caption(
        "Decision Support System"
    )

    st.sidebar.markdown("---")

    # =====================================
    # NAVIGATION
    # =====================================

    menu = st.sidebar.radio(
        "Select Module",
        [
            "🏠 Dashboard",
            "📊 Data-Driven DSS",
            "⚖️ Criteria Weight",
            "📋 Payoff Table",
            "🎲 EV & EOL",
            "❓ Uncertainty",
            "📈 Distribution",
            "⚖️ Utility Function",
            "🎰 Monte Carlo",
            "🏆 Recommendation"
        ]
    )

    st.sidebar.markdown("---")

    # =====================================
    # SYSTEM STATUS
    # =====================================

    st.sidebar.subheader(
        "🔗 System Status"
    )

    payoff_exists = (
        "payoff_df" in st.session_state
        and st.session_state["payoff_df"] is not None
        and isinstance(
            st.session_state["payoff_df"],
            pd.DataFrame
        )
        and not st.session_state["payoff_df"].empty
    )

    if payoff_exists:

        payoff_df = st.session_state[
            "payoff_df"
        ]

        st.sidebar.success(
            "✅ Payoff Connected"
        )

        if (
            "weighted_payoff_df"
            in st.session_state
        ):

            st.sidebar.success(
                "✅ Weighted Matrix Ready"
            )

        if (
            "final_recommendation"
            in st.session_state
        ):

            st.sidebar.success(
                "✅ Recommendation Ready"
            )

        st.sidebar.metric(
            "Alternatives",
            payoff_df.shape[0]
        )

        st.sidebar.metric(
            "Criteria",
            payoff_df.shape[1]
        )

        st.sidebar.metric(
            "Total Cells",
            payoff_df.shape[0]
            *
            payoff_df.shape[1]
        )

    else:

        st.sidebar.warning(
            "⚠️ No Payoff Data"
        )

    # =====================================
    # WORKFLOW PROGRESS
    # =====================================

    st.sidebar.markdown("---")

    st.sidebar.subheader(
        "🚀 Workflow Progress"
    )

    progress = 0

    if (
        "uploaded_df" in st.session_state
        and st.session_state["uploaded_df"] is not None
    ):
        progress += 10

    if (
        "payoff_df" in st.session_state
        and st.session_state["payoff_df"] is not None
    ):
        progress += 20

    if (
        "criteria_weights" in st.session_state
    ):
        progress += 20

    if (
        "ev_result" in st.session_state
    ):
        progress += 15

    if (
        "final_recommendation"
        in st.session_state
    ):
        progress += 35

    st.sidebar.progress(
        progress / 100
    )

    st.sidebar.write(
        f"{progress}% Completed"
    )

    # =====================================
    # CURRENT RECOMMENDATION
    # =====================================

    if (
        "final_recommendation"
        in st.session_state
    ):

        st.sidebar.markdown("---")

        st.sidebar.subheader(
            "🏆 Current Recommendation"
        )

        st.sidebar.success(
            st.session_state[
                "final_recommendation"
            ]
        )

    # =====================================
    # CRITERIA WEIGHTS
    # =====================================

    if (
        "criteria_weights"
        in st.session_state
    ):

        st.sidebar.markdown("---")

        st.sidebar.subheader(
            "⚖️ Criteria Weights"
        )

        weights = st.session_state[
            "criteria_weights"
        ]

        for k, v in weights.items():

            st.sidebar.write(
                f"{k}: {round(v,2)}"
            )

    # =====================================
    # FOOTER
    # =====================================

    st.sidebar.markdown("---")

    st.sidebar.caption(
        "Developed by Auta Shintha Sarah"
    )

    return menu
