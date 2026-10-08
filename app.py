import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="IPL Match Analytics & Intelligence",
    page_icon="🏏",
    layout="wide"
)

# ----------------- HISTORICAL & METADATA -----------------
teams = [
    "Chennai Super Kings",
    "Delhi Capitals",
    "Gujarat Titans",
    "Kolkata Knight Riders",
    "Lucknow Super Giants",
    "Mumbai Indians",
    "Punjab Kings",
    "Rajasthan Royals",
    "Royal Challengers Bengaluru",
    "Sunrisers Hyderabad"
]

team_profiles = {
    "Chennai Super Kings": {"titles": 5, "finals": 10, "win_pct": 58.2, "highest": 246, "lowest": 79},
    "Mumbai Indians": {"titles": 5, "finals": 6, "win_pct": 56.4, "highest": 247, "lowest": 87},
    "Kolkata Knight Riders": {"titles": 3, "finals": 4, "win_pct": 52.1, "highest": 272, "lowest": 67},
    "Gujarat Titans": {"titles": 1, "finals": 2, "win_pct": 62.5, "highest": 233, "lowest": 89},
    "Rajasthan Royals": {"titles": 1, "finals": 2, "win_pct": 50.8, "highest": 226, "lowest": 58},
    "Sunrisers Hyderabad": {"titles": 1, "finals": 3, "win_pct": 49.3, "highest": 287, "lowest": 96},
    "Royal Challengers Bengaluru": {"titles": 0, "finals": 3, "win_pct": 48.7, "highest": 263, "lowest": 49},
    "Delhi Capitals": {"titles": 0, "finals": 1, "win_pct": 45.9, "highest": 257, "lowest": 66},
    "Punjab Kings": {"titles": 0, "finals": 1, "win_pct": 45.2, "highest": 262, "lowest": 73},
    "Lucknow Super Giants": {"titles": 0, "finals": 0, "win_pct": 54.3, "highest": 257, "lowest": 108}
}

venues_data = {
    "Wankhede Stadium, Mumbai": {"avg_score": 185, "bias": "chase", "chase_win_pct": "57%"},
    "M Chinnaswamy Stadium, Bengaluru": {"avg_score": 190, "bias": "chase", "chase_win_pct": "60%"},
    "MA Chidambaram Stadium, Chepauk, Chennai": {"avg_score": 165, "bias": "defend", "chase_win_pct": "46%"},
    "Eden Gardens, Kolkata": {"avg_score": 182, "bias": "chase", "chase_win_pct": "55%"},
    "Narendra Modi Stadium, Ahmedabad": {"avg_score": 178, "bias": "chase", "chase_win_pct": "54%"},
    "Arun Jaitley Stadium, Delhi": {"avg_score": 172, "bias": "defend", "chase_win_pct": "48%"},
    "Rajiv Gandhi International Stadium, Hyderabad": {"avg_score": 180, "bias": "defend", "chase_win_pct": "49%"},
    "Punjab Cricket Association IS Bindra Stadium, Mohali": {"avg_score": 176, "bias": "chase", "chase_win_pct": "56%"}
}

team_strengths = {
    "Chennai Super Kings": {"base": 1.25, "batting": 8.7, "bowling": 8.8},
    "Mumbai Indians": {"base": 1.22, "batting": 9.0, "bowling": 8.5},
    "Kolkata Knight Riders": {"base": 1.16, "batting": 8.8, "bowling": 8.4},
    "Gujarat Titans": {"base": 1.15, "batting": 8.3, "bowling": 8.7},
    "Royal Challengers Bengaluru": {"base": 1.14, "batting": 9.1, "bowling": 7.9},
    "Rajasthan Royals": {"base": 1.10, "batting": 8.5, "bowling": 8.6},
    "Sunrisers Hyderabad": {"base": 1.08, "batting": 8.9, "bowling": 8.2},
    "Lucknow Super Giants": {"base": 1.05, "batting": 8.2, "bowling": 8.3},
    "Delhi Capitals": {"base": 0.98, "batting": 8.1, "bowling": 8.0},
    "Punjab Kings": {"base": 0.92, "batting": 8.0, "bowling": 7.8}
}

team_key_players = {
    "Chennai Super Kings": ["Ruturaj Gaikwad (C)", "MS Dhoni (WK)", "Ravindra Jadeja", "Matheesha Pathirana"],
    "Mumbai Indians": ["Rohit Sharma", "Suryakumar Yadav", "Jasprit Bumrah", "Hardik Pandya (C)"],
    "Kolkata Knight Riders": ["Shreyas Iyer (C)", "Andre Russell", "Sunil Narine", "Rinku Singh"],
    "Gujarat Titans": ["Shubman Gill (C)", "Rashid Khan", "David Miller", "Sai Sudharsan"],
    "Royal Challengers Bengaluru": ["Virat Kohli", "Faf du Plessis (C)", "Glenn Maxwell", "Mohammed Siraj"],
    "Rajasthan Royals": ["Sanju Samson (C)", "Jos Buttler", "Yashasvi Jaiswal", "Yuzvendra Chahal"],
    "Sunrisers Hyderabad": ["Pat Cummins (C)", "Travis Head", "Heinrich Klaasen (WK)", "Abhishek Sharma"],
    "Lucknow Super Giants": ["KL Rahul (C)", "Nicholas Pooran (WK)", "Marcus Stoinis", "Ravi Bishnoi"],
    "Delhi Capitals": ["Rishabh Pant (C)", "Axar Patel", "Kuldeep Yadav", "Tristan Stubbs"],
    "Punjab Kings": ["Shikhar Dhawan", "Sam Curran (C)", "Arshdeep Singh", "Liam Livingstone"]
}

# ----------------- SIDEBAR -----------------
with st.sidebar:
    st.header("⚙️ Project Architecture")
    st.markdown("""
    **Core Engine Parameters:**
    - 📊 Franchise Historical Ratings & Titles
    - 🏟️ Pitch & Venue Chase Bias
    - 🪙 Toss Decision Dynamics
    - ⭐ Active Impact Star Squads
    - 🌧️ DLS Rain Cutoff Calculations
    - ⏱️ 2nd Innings CRR vs RRR Pressure
    - 📈 Projected 1st Innings Par Scores
    """)
    st.divider()
    st.markdown("**Repository:** [GitHub IPL Analytics](https://github.com/Anukram01/IPL--DATA-ANALYTICS-)")
    st.caption("Developed by Anukram Sachan")

# ----------------- MAIN TABS -----------------
st.title("🏏 IPL Match Intelligence Dashboard")
tab1, tab2, tab3 = st.tabs([
    "🔮 Pre-Match Outcome Predictor", 
    "⚡ Live Chase & DLS Simulator",
    "📚 Franchise Records & Head-to-Head"
])

# ================= TAB 1: PRE-MATCH PREDICTOR =================
with tab1:
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        team1 = st.selectbox("Select Team 1", teams, index=teams.index("Royal Challengers Bengaluru"), key="pm_t1")
    with col_
    
