# -*- coding: utf-8 -*-

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px


def show_ev_eol():

    st.title("🎲 EV & EOL Analysis")

    st.write("""
    Expected Value (EV) digunakan untuk memilih
    alternatif dengan nilai harapan tertinggi.

    Expected Opportunity Loss (EOL) digunakan
    untuk memilih alternatif dengan kerugian
    peluang terkecil.
    """)

    # =====================================
    # VALIDATION
    # =====================================

    if (
        "criteria_weights" not in st.session_state
    ):

        st.warning(
            "⚠️ Configure criteria weights first."
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
    # MATRIX DISPLAY
    # =====================================

    st.subheader(
        "📊 Weighted Payoff Matrix"
    )

    st.dataframe(
        payoff_df,
        use_container_width=True
    )

    # =====================================
    # EV CALCULATION
    # =====================================

    ev = payoff_df.dot(weights)

    ev_df = pd.DataFrame({

        "Alternative": payoff_df.index,

        "EV Score": np.round(
            ev.values,
            4
        )

    })

    ev_df = ev_df.sort_values(
        by="EV Score",
        ascending=False
    )

    # =====================================
    # EV TABLE
    # =====================================

    st.subheader(
        "🎯 Expected Value Ranking"
    )

    st.dataframe(
        ev_df,
        use_container_width=True
    )

    # =====================================
    # EV CHART
    # =====================================

    fig_ev = px.bar(
        ev_df,
        x="Alternative",
        y="EV Score",
        color="EV Score",
        color_continuous_scale="Brwnyl",
        title="Expected Value Ranking"
    )

    st.plotly_chart(
        fig_ev,
        use_container_width=True
    )

    # =====================================
    # EOL CALCULATION
    # =====================================

    regret = payoff_df.max() - payoff_df

    eol = regret.dot(weights)

    eol_df = pd.DataFrame({

        "Alternative": payoff_df.index,

        "EOL Score": np.round(
            eol.values,
            4
        )

    })

    eol_df = eol_df.sort_values(
        by="EOL Score",
        ascending=True
    )

    # =====================================
    # EOL TABLE
    # =====================================

    st.subheader(
        "📉 Expected Opportunity Loss Ranking"
    )

    st.dataframe(
        eol_df,
        use_container_width=True
    )

    # =====================================
    # EOL CHART
    # =====================================

    fig_eol = px.bar(
        eol_df,
        x="Alternative",
        y="EOL Score",
        color="EOL Score",
        color_continuous_scale="Brwnyl",
        title="Expected Opportunity Loss Ranking"
    )

    st.plotly_chart(
        fig_eol,
        use_container_width=True
    )

    # =====================================
    # BEST RESULT
    # =====================================

    best_ev = ev.idxmax()

    best_eol = eol.idxmin()

    st.subheader(
        "🏆 Best Alternative"
    )

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Best EV",
            best_ev
        )

    with col2:

        st.metric(
            "Best EOL",
            best_eol
        )

    # =====================================
    # INTERPRETATION
    # =====================================

    st.subheader(
        "📝 Interpretation"
    )

    if best_ev == best_eol:

        st.success(
            f"""
            Lokasi {best_ev}
            dipilih oleh EV dan EOL.

            Hal ini menunjukkan bahwa
            lokasi tersebut memiliki
            keuntungan tertinggi sekaligus
            risiko opportunity loss terendah.
            """
        )

    else:

        st.info(
            f"""
            EV memilih {best_ev}
            sebagai alternatif terbaik.

            EOL memilih {best_eol}
            sebagai alternatif terbaik.

            Perbedaan hasil menunjukkan
            adanya trade-off antara
            keuntungan dan risiko.
            """
        )

    # =====================================
    # TOP 3 EV
    # =====================================

    st.subheader(
        "🥇 Top 3 EV Alternatives"
    )

    top3_ev = ev_df.head(3)

    st.dataframe(
        top3_ev,
        use_container_width=True
    )

    # =====================================
    # TOP 3 EOL
    # =====================================

    st.subheader(
        "🥇 Top 3 EOL Alternatives"
    )

    top3_eol = eol_df.head(3)

    st.dataframe(
        top3_eol,
        use_container_width=True
    )

    # =====================================
    # SAVE SESSION
    # =====================================

    st.session_state[
        "ev_result"
    ] = best_ev

    st.session_state[
        "eol_result"
    ] = best_eol

    st.session_state[
        "ev_table"
    ] = ev_df

    st.session_state[
        "eol_table"
    ] = eol_df
