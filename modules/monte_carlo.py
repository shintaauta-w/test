import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px


def show_monte_carlo():

    st.title("🎰 Monte Carlo Simulation")

    st.write("""
    Monte Carlo Simulation digunakan untuk
    mensimulasikan ribuan kemungkinan hasil
    berdasarkan distribusi payoff setiap lokasi.
    """)

    # =====================================
    # VALIDATION
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
    # SIMULATION SETTING
    # =====================================

    simulations = st.slider(
        "Number of Simulations",
        min_value=100,
        max_value=10000,
        value=5000,
        step=100
    )

    # =====================================
    # RUN SIMULATION
    # =====================================

    results = []

    for location in payoff_df.index:

        values = payoff_df.loc[
            location
        ].values

        mean_value = np.mean(values)

        std_value = np.std(values)

        simulated = np.random.normal(
            mean_value,
            std_value,
            simulations
        )

        probability_profit = (
            np.mean(simulated > 0)
            * 100
        )

        results.append({

            "Location":
            location,

            "Expected Profit":
            np.mean(simulated),

            "Risk (Std)":
            np.std(simulated),

            "Probability Profit (%)":
            probability_profit,

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

    result_df = result_df.round(4)

    # =====================================
    # DISPLAY TABLE
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

    best_location = result_df.iloc[0][
        "Location"
    ]

    best_profit = result_df.iloc[0][
        "Expected Profit"
    ]

    best_probability = result_df.iloc[0][
        "Probability Profit (%)"
    ]

    # =====================================
    # METRICS
    # =====================================

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Best Location",
            best_location
        )

    with col2:

        st.metric(
            "Expected Profit",
            round(best_profit, 4)
        )

    with col3:

        st.metric(
            "Profit Probability",
            f"{round(best_probability,2)}%"
        )

    # =====================================
    # EXPECTED PROFIT CHART
    # =====================================

    st.subheader(
        "📈 Expected Profit Comparison"
    )

    fig_profit = px.bar(
        result_df,
        x="Location",
        y="Expected Profit",
        color="Expected Profit",
        color_continuous_scale="Brwnyl"
    )

    st.plotly_chart(
        fig_profit,
        use_container_width=True
    )

    # =====================================
    # RISK CHART
    # =====================================

    st.subheader(
        "⚠️ Risk Comparison"
    )

    fig_risk = px.bar(
        result_df,
        x="Location",
        y="Risk (Std)",
        color="Risk (Std)",
        color_continuous_scale="Reds"
    )

    st.plotly_chart(
        fig_risk,
        use_container_width=True
    )

    # =====================================
    # RISK RETURN MAP
    # =====================================

    st.subheader(
        "🎯 Risk vs Return"
    )

    fig_scatter = px.scatter(
        result_df,
        x="Risk (Std)",
        y="Expected Profit",
        size="Probability Profit (%)",
        color="Location",
        hover_name="Location"
    )

    st.plotly_chart(
        fig_scatter,
        use_container_width=True
    )

    # =====================================
    # SAVE SESSION
    # =====================================

    st.session_state[
        "monte_carlo_result"
    ] = best_location

    st.session_state[
        "monte_carlo_table"
    ] = result_df

    # =====================================
    # FINAL RESULT
    # =====================================

    st.success(
        f"🏆 Best Monte Carlo Location : {best_location}"
    )

    st.info(
        f"""
        Expected Profit = {round(best_profit,4)}

        Probability of Profit = {round(best_probability,2)}%
        """
    )
