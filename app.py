import streamlit as st
import pandas as pd

st.set_page_config(page_title="IPL Match Outcome Predictor", page_icon="🏏", layout="centered")

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

# Franchise Strength Ratings (Base, Batting, Bowling on a scale of 10)
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

st.title("🏏 IPL Match Outcome Predictor")
st.caption("Forecasting win probabilities using historical analytics, toss dynamics, player availability, and pitch factors.")

team1 = st.selectbox("Select Team 1", teams, index=teams.index("Royal Challengers Bengaluru"))
remaining_teams = [t for t in teams if t != team1]
team2 = st.selectbox("Select Team 2", remaining_teams, index=remaining_teams.index("Chennai Super Kings") if "Chennai Super Kings" in remaining_teams else 0)

venue = st.selectbox("Select Venue", list(venues_data.keys()))

# 1. Venue Insights Section
v_info = venues_data[venue]
v_col1, v_col2, v_col3 = st.columns(3)
v_col1.metric("Avg 1st Innings", f"{v_info['avg_score']} runs")
v_col2.metric("Chasing Win Rate", v_info["chase_win_pct"])
v_col3.metric("Favorable Strategy", "Chase & Bowl 1st" if v_info["bias"] == "chase" else "Defend & Bat 1st")

col1, col2 = st.columns(2)
with col1:
    toss_winner = st.selectbox("Toss Winner", [team1, team2])
with col2:
    toss_decision = st.selectbox("Toss Decision", ['bat', 'field'])

# 2. Key Players Selection
with st.expander("⭐ Select In-Form Impact Players (Live Form Factor)"):
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        st.markdown(f"**{team1} Stars**")
        selected_p1 = [p for p in team_key_players.get(team1, []) if st.checkbox(p, value=True, key=f"t1_{p}")]
    with col_p2:
        st.markdown(f"**{team2} Stars**")
        selected_p2 = [p for p in team_key_players.get(team2, []) if st.checkbox(p, value=True, key=f"t2_{p}")]

st.write("")

if st.button("Predict Win Probability", type="primary", use_container_width=True):
    r1 = team_strengths[team1]["base"]
    r2 = team_strengths[team2]["base"]

    # Toss impact (+4%)
    if toss_winner == team1:
        r1 *= 1.04
    else:
        r2 *= 1.04

    # Venue strategy match (+4%)
    if (v_info["bias"] == "chase" and toss_decision == "field") or (v_info["bias"] == "defend" and toss_decision == "bat"):
        if toss_winner == team1:
            r1 *= 1.04
        else:
            r2 *= 1.04

    # Active impact players factor
    r1 *= (1 + (len(selected_p1) * 0.03))
    r2 *= (1 + (len(selected_p2) * 0.03))

    p1 = (r1 / (r1 + r2)) * 100
    p2 = 100 - p1

    st.divider()
    st.subheader("Match Outcome Probability")
    st.progress(int(p1))
    
    st.write(f"**{team1}**: `{round(p1, 1)}%` (Active Stars: {len(selected_p1)})")
    st.write(f"**{team2}**: `{round(p2, 1)}%` (Active Stars: {len(selected_p2)})")

    if p1 > p2:
        st.success(f"🏆 Favored Winner: **{team1}**")
    else:
        st.success(f"🏆 Favored Winner: **{team2}**")

    # 3. Visual Matchup Chart (Batting, Bowling & Win Probability Comparison)
    st.subheader("📊 Head-to-Head Squad Matchup")
    comparison_df = pd.DataFrame({
        "Attribute": ["Batting Index (/10)", "Bowling Index (/10)", "Calculated Win %"],
        team1: [team_strengths[team1]["batting"], team_strengths[team1]["bowling"], round(p1, 1)],
        team2: [team_strengths[team2]["batting"], team_strengths[team2]["bowling"], round(p2, 1)]
    }).set_index("Attribute")
    
    st.bar_chart(comparison_df)

    # 4. Factor Breakdown Details
    with st.expander("🔍 Match Factor Breakdown"):
        st.write(f"- **Toss Advantage:** Claimed by `{toss_winner}` by choosing to `{toss_decision}`.")
        strategy_matched = (v_info["bias"] == "chase" and toss_decision == "field") or (v_info["bias"] == "defend" and toss_decision == "bat")
        st.write(f"- **Pitch Strategy Alignment:** {'Aligned with stadium dynamics' if strategy_matched else 'Against historical stadium trend'}.")
        st.write(f"- **Active Impact Core:** `{team1}` ({len(selected_p1)} active) vs `{team2}` ({len(selected_p2)} active).")
        
