import streamlit as st


def show_dashboard():

    st.title("🤎 Business Location DSS")

    st.write("""
    Sistem Pendukung Keputusan
    untuk menentukan lokasi usaha terbaik
    menggunakan berbagai metode DSS.
    """)

    # =====================================
    # CHECK SESSION
    # =====================================

    if (
        "payoff_df" in st.session_state
        and st.session_state["payoff_df"] is not None
    ):

        total_loc = len(
            st.session_state["payoff_df"]
        )

        total_state = len(
            st.session_state["payoff_df"].columns
        )

        status = "Connected"

    else:

        total_loc = 0
        total_state = 0
        status = "Waiting"

    # =====================================
    # METRICS
    # =====================================

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "📊 Modules",
            10
        )

    with col2:
        st.metric(
            "📍 Locations",
            total_loc
        )

    with col3:
        st.metric(
            "🌎 Criteria",
            total_state
        )

    with col4:
        st.metric(
            "🏆 Status",
            status
        )

    # =====================================
    # BEST RECOMMENDATION
    # =====================================

    st.markdown("---")

    st.subheader(
        "🏆 Current Best Recommendation"
    )

    final_rec = st.session_state.get(
        "final_recommendation",
        None
    )

    if final_rec is not None:

        st.success(
            f"Lokasi terbaik saat ini: {final_rec}"
        )

        if (
            "ranking_df" in st.session_state
            and st.session_state["ranking_df"] is not None
        ):

            ranking_df = st.session_state[
                "ranking_df"
            ]

            if len(ranking_df) > 0:

                col1, col2 = st.columns(2)

                with col1:

                    st.metric(
                        "🥇 Top Location",
                        ranking_df.iloc[0]["Location"]
                    )

                with col2:

                    if "Votes" in ranking_df.columns:

                        st.metric(
                            "🗳️ Votes",
                            ranking_df.iloc[0]["Votes"]
                        )

    else:

        st.info(
            "Belum ada rekomendasi akhir."
        )

    # =====================================
    # WORKFLOW
    # =====================================

    st.markdown("---")

    st.subheader(
        "🚀 Workflow"
    )

    st.info("""
    1. Upload dataset

    2. Generate payoff matrix

    3. Set criteria weights

    4. Run EV & EOL analysis

    5. Analyze uncertainty

    6. Distribution analysis

    7. Utility analysis

    8. Monte Carlo simulation

    9. Final recommendation
    """)

    # =====================================
    # CONNECTION STATUS
    # =====================================

    st.markdown("---")

    st.subheader(
        "🔗 System Connection"
    )

    if status == "Connected":

        st.success("""
        ✅ Dataset Connected

        ✅ Payoff Matrix Connected

        ✅ All DSS Modules Connected
        """)

    else:

        st.warning("""
        ⚠️ Upload dataset terlebih dahulu
        untuk menghubungkan semua module DSS.
        """)

    # =====================================
    # DSS METHODS
    # =====================================

    st.markdown("---")

    st.subheader(
        "📌 DSS Methods"
    )

    st.write("""
    Sistem ini menggunakan beberapa metode
    pengambilan keputusan untuk menentukan
    lokasi usaha terbaik.

    Metode yang digunakan:

    • Expected Value (EV)

    • Expected Opportunity Loss (EOL)

    • Maximax

    • Maximin

    • Laplace

    • Minimax Regret

    • Utility Function

    • Monte Carlo Simulation

    Seluruh metode akan digabungkan
    pada Recommendation Engine
    untuk menghasilkan keputusan akhir.
    """)

    # =====================================
    # PROJECT INFORMATION
    # =====================================

    st.markdown("---")

    st.subheader(
        "ℹ️ Project Information"
    )

    st.info("""
    Business Location DSS merupakan
    Sistem Pendukung Keputusan (SPK)
    yang membantu investor atau pemilik usaha
    memilih lokasi bisnis terbaik berdasarkan
    berbagai kriteria dan metode analisis keputusan.

    Developed by:
    Auta Shintha Sarah

    Course:
    Teori Pengambilan Keputusan (TPK)
    """)
