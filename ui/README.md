# 🤎 Business Location DSS

## 📌 Overview

Business Location DSS adalah Sistem Pendukung Keputusan (Decision Support System) untuk membantu menentukan lokasi usaha terbaik berdasarkan berbagai kriteria bisnis.

Sistem ini dibangun menggunakan Python dan Streamlit serta mengimplementasikan beberapa metode pengambilan keputusan untuk mendukung pemilihan lokasi usaha secara objektif.

---

## 🚀 Features

- Upload dataset CSV/XLSX
- Generate Payoff Matrix
- Criteria Weighting
- Expected Value (EV)
- Expected Opportunity Loss (EOL)
- Maximax
- Maximin
- Laplace
- Minimax Regret
- Distribution Analysis
- Utility Function Analysis
- Monte Carlo Simulation
- Final Recommendation Engine

---

## 📊 DSS Workflow

1. Upload Dataset
2. Generate Payoff Matrix
3. Set Criteria Weights
4. EV & EOL Analysis
5. Uncertainty Analysis
6. Distribution Analysis
7. Utility Analysis
8. Monte Carlo Simulation
9. Recommendation Engine

---

## 🛠️ Technologies

- Python
- Streamlit
- Pandas
- NumPy
- Plotly

---

## 📁 Project Structure

```text
Business-Location-DSS/
│
├── modules/
│   ├── dashboard.py
│   ├── data_driven.py
│   ├── criteria_weight.py
│   ├── payoff_table.py
│   ├── ev_eol.py
│   ├── uncertainty.py
│   ├── distribution.py
│   ├── utility.py
│   ├── monte_carlo.py
│   └── recommendation_engine.py
│
├── ui/
│   ├── sidebar.py
│   └── styles.py
│
├── app.py
├── config.py
├── requirements.txt
└── README.md
```

---

## ▶️ Run Application

Install dependencies:

```bash
pip install -r requirements.txt
```

Run Streamlit:

```bash
streamlit run app.py
```

---

## 👩‍💻 Developer

Auta Shintha Sarah

Program Studi Statistika

Universitas Negeri Medan

---

## 📚 Course

Teori Pengambilan Keputusan (TPK)

Decision Support System Project
