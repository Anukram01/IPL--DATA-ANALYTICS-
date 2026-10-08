# 🏏 IPL Match Intelligence & Analytics Platform

An end-to-end interactive cricket analytics and outcome simulation dashboard built with **Python**, **Streamlit**, and **Pandas**. The platform combines historical franchise statistics, venue pitch dynamics, toss impact, squad availability, and dynamic DLS rain-reduction rules to deliver real-time match predictions and deep squad insights.

---

### 🚀 Live Interactive Demo
👉 **[Launch Live IPL Dashboard](https://ipl-prediction-anukram2.streamlit.app/)**

---

## 📌 Key Architectural Features

### 1. 🔮 Pre-Match Outcome Predictor
- **Dynamic Multi-Factor Modeling:** Computes win probabilities using historical franchise base strengths, toss decisions, and venue-specific chasing bias.
- **Active Impact Star Selector:** Real-time squad availability toggles that adjust team ratings dynamically based on playing XI match-winners.
- **1st Innings Par & Powerplay Estimator:** Predicts expected target score ranges and powerplay scores based on stadium historical averages and batting indices.
- **Visual Squad Index Comparison:** Head-to-head comparative chart displaying Batting Index, Bowling Strength, and Win Likelihood.
- **Exportable Match Report:** Single-click download of a formatted `Match Intelligence Report (.txt)` for technical summaries.

### 2. ⚡ Live In-Match Chase & DLS Simulator
- **Real-Time Pressure Engine:** Calculates live 2nd-innings win probabilities using Required Run Rate (RRR) vs. Current Run Rate (CRR) delta and wickets in hand.
- **🌧️ DLS Rain Revision Engine:** Simulates rain interruptions with shortened match overs (5 to 19 overs), automatically recalculating revised targets and escalating run-rate requirements.

### 3. 📚 Franchise Records & Head-to-Head Explorer
- Interactive multi-season historical comparison of IPL franchises.
- Evaluates career win percentages, tournament titles, finals appearances, and highest/lowest total records.

---

## 🛠️ Tech Stack & Libraries
- **Language:** Python
- **Dashboard Framework:** Streamlit
- **Data Manipulation & Analytics:** Pandas
- **Exploratory Analytics & Queries:** SQL / SQLite
- **Deployment:** Streamlit Cloud & GitHub

---

## 💻 How to Run Locally

If you prefer to run and inspect the application on your local machine:

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/Anukram01/IPL--DATA-ANALYTICS-.git](https://github.com/Anukram01/IPL--DATA-ANALYTICS-.git)
   cd IPL--DATA-ANALYTICS-
   
