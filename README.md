# 🏏 IPL Match & Franchise Analytics (2008–Present)

### 📌 Project Overview
An end-to-end exploratory data analytics and SQL querying project evaluating historical Indian Premier League (IPL) match records. The objective is to extract data-driven insights into venue-specific toss conversion efficiency, team victory margin distributions, and historical franchise ground dominance.

---

### 🔍 Key Analytical Findings
- **Venue Toss Conversion Bias:** Certain stadiums demonstrate a notable toss-winner match conversion rate (>55%), highlighting chasing advantages and dew impact.
- **Victory Margin Patterns:** Quantified average winning margins across target-defending vs chasing dynamics, isolating high-impact blowout victories (>50 runs or 8+ wickets).
- **Franchise Ground Dominance:** Identified top multi-season winning franchises and their venue-specific win conversion rates.

---

### 🛠️ Tech Stack
- **Languages:** Python (Pandas, Matplotlib, Seaborn), SQL
- **Database / Query Engine:** SQLite
- **Environment:** Google Colab / Jupyter Notebook

---

### 📊 SQL Analytical Highlights
Included in `queries.sql`:
1. **Venue-Wise Toss Conversion Efficiency:** Calculates match win percentages when a team wins both the toss and the match across grounds with ≥ 15 fixtures.
2. **Dominant Victories Extraction:** Filters high-margin blowout victories by runs and wickets to evaluate squad dominance.
3. 
