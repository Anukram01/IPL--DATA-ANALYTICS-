import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="IPL Match Analytics & Predictor",
    page_icon="🏏",
    layout="wide"
)

# ----------------- DATA & CONSTANTS -----------------
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
    **Model Features Considered:**
    - 📊 Franchise Historical Ratings
    - 🏟️ Pitch & Venue Chase Bias
    - 🪙 Toss Decision Dynamics
    - ⭐ Active Impact Star Factor
    - ⏱️ In-Match Run Rate Pressures
    """)
    st.divider()
    st.markdown("**Repository:** [GitHub IPL Analytics](https://github.com/Anukram01/IPL--DATA-ANALYTICS-)")
    st.caption("Developed by Anukram Sachan")

# ----------------- MAIN APP TABS -----------------
st.title("🏏 IPL Match Intelligence & Analytics")
tab1, tab2 = st.tabs(["🔮 Pre-Match Outcome Predictor", "⚡ Live Chase In-Match Simulator"])

# ================= TAB 1: PRE-MATCH PREDICTOR =================
with tab1:
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        team1 = st.selectbox("Select Team 1", teams, index=teams.index("Royal Challengers Bengaluru"), key="pm_t1")
    with col_t2:
        remaining_teams = [t for t in teams if t != team1]
        team2 = st.selectbox("Select Team 2", remaining_teams, index=remaining_teams.index("Chennai Super Kings") if "Chennai Super Kings" in remaining_teams else 0, key="pm_t2")

    venue = st.selectbox("Select Venue", list(venues_data.keys()), key="pm_venue")

    # Venue Insights Cards
    v_info = venues_data[venue]
    vc1, vc2, vc3 = st.columns(3)
    vc1.metric("Avg 1st Innings Score", f"{v_info['avg_score']} runs")
    vc2.metric("Chasing Win Rate", v_info["chase_win_pct"])
    vc3.metric("Venue Recommendation", "Chase & Field" if v_info["bias"] == "chase" else "Defend & Bat")

    c_toss1, c_toss2 = st.columns(2)
    with c_toss1:
        toss_winner = st.selectbox("Toss Winner", [team1, team2], key="pm_toss_win")
    with c_toss2:
        toss_decision = st.selectbox("Toss Decision", ['bat', 'field'], key="pm_toss_dec")

    with st.expander("⭐ Select In-Form Impact Players (Live Form Factor)"):
        pcol1, pcol2 = st.columns(2)
        with pcol1:
            st.markdown(f"**{team1} Stars**")
            selected_p1 = [p for p in team_key_players.get(team1, []) if st.checkbox(p, value=True, key=f"t1_star_{p}")]
        with pcol2:
            st.markdown(f"**{team2} Stars**")
            selected_p2 = [p for p in team_key_players.get(team2, []) if st.checkbox(p, value=True, key=f"t2_star_{p}")]

    st.write("")
    if st.button("Predict Match Outcome", type="primary", use_container_width=True, key="pm_btn"):
        r1 = team_strengths[team1]["base"]
        r2 = team_strengths[team2]["base"]

        # Toss Edge (+4%)
        if toss_winner == team1:
            r1 *= 1.04
        else:
            r2 *= 1.04

        # Pitch strategy alignment (+4%)
        if (v_info["bias"] == "chase" and toss_decision == "field") or (v_info["bias"] == "defend" and toss_decision == "bat"):
            if toss_winner == team1:
                r1 *= 1.04
            else:
                r2 *= 1.04

        # Active player form factor
        r1 *= (1 + (len(selected_p1) * 0.03))
        r2 *= (1 + (len(selected_p2) * 0.03))

        p1 = (r1 / (r1 + r2)) * 100
        p2 = 100 - p1

        st.divider()
        st.subheader("Match Outcome Probability")
        st.progress(int(p1))
        
        st.write(f"**{team1}**: `{round(p1, 1)}%` (Active Stars: {len(selected_p1)})")
        st.write(f"**{team2}**: `{round(p2, 1)}%` (Active Stars: {len(selected_p2)})")

        favored = team1 if p1 > p2 else team2
        st.success(f"🏆 Favored Winner: **{favored}**")

        # Head to Head squad matchup chart
        st.subheader("📊 Squad Index Comparison")
        comp_df = pd.DataFrame({
            "Metric": ["Batting Index (/10)", "Bowling Index (/10)", "Win Likelihood %"],
            team1: [team_strengths[team1]["batting"], team_strengths[team1]["bowling"], round(p1, 1)],
            team2: [team_strengths[team2]["batting"], team_strengths[team2]["bowling"], round(p2, 1)]
        }).set_index("Metric")
        st.bar_chart(comp_df)

        # Download Match Intelligence Report
        report_text = f"""=== IPL MATCH INTELLIGENCE REPORT ===
Matchup: {team1} vs {team2}
Venue: {venue}
Avg 1st Innings: {v_info['avg_score']} | Chasing Win Rate: {v_info['chase_win_pct']}
Toss Winner: {toss_winner} (Chose to {toss_decision})
Predicted Win Probabilities:
  - {team1}: {round(p1, 1)}%
  - {team2}: {round(p2, 1)}%
Favored Winner: {favored}
======================================
"""
        st.download_button(
            label="📥 Download Match Intelligence Report",
            data=report_text,
            file_name=f"IPL_Match_Report_{team1}_vs_{team2}.txt",
            mime="text/plain",
            use_container_width=True
        )

# ================= TAB 2: LIVE CHASE SIMULATOR =================
with tab2:
    st.subheader("⚡ 2nd Innings Real-Time Chase Probability")
    st.caption("Calculate live win chance under current overs, wickets, and run rate pressure.")

    sim_c1, sim_c2 = st.columns(2)
    with sim_c1:
        chasing_team = st.selectbox("Chasing Team (Batting 2nd)", teams, index=teams.index("Royal Challengers Bengaluru"), key="live_chasing")
    with sim_c2:
        defending_team = st.selectbox("Defending Team (Bowling 2nd)", [t for t in teams if t != chasing_team], index=0, key="live_defending")

    sc1, sc2, sc3, sc4 = st.columns(4)
    with sc1:
        target = st.number_input("Target Score", min_value=50, max_value=300, value=185, step=1)
    with sc2:
        current_score = st.number_input("Current Runs", min_value=0, max_value=300, value=98, step=1)
    with sc3:
        wickets_down = st.number_input("Wickets Fallen", min_value=0, max_value=9, value=2, step=1)
    with sc4:
        overs_done = st.number_input("Overs Completed", min_value=1.0, max_value=19.5, value=11.4, step=0.1)

    # Calculation logic for in-play state
    legal_balls = int(overs_done) * 6 + int(round((overs_done - int(overs_done)) * 10))
    balls_left = max(1, 120 - legal_balls)
    runs_needed = max(0, target - current_score)
    wickets_left = 10 - wickets_down

    crr = current_score / (legal_balls / 6) if legal_balls > 0 else 0
    rrr = runs_needed / (balls_left / 6) if balls_left > 0 else 0

    mc1, mc2, mc3, mc4 = st.columns(4)
    mc1.metric("Runs Needed", runs_needed)
    mc2.metric("Balls Remaining", balls_left)
    mc3.metric("Current Run Rate (CRR)", f"{crr:.2f}")
    mc4.metric("Required Run Rate (RRR)", f"{rrr:.2f}")

    if st.button("Calculate Live Situation Odds", type="primary", use_container_width=True, key="live_calc_btn"):
        if runs_needed <= 0:
            st.success(f"🎉 {chasing_team} has reached the target and won the match!")
        else:
            # Baseline probability from remaining wickets & run-rate gap
            rate_delta = crr - rrr
            base_chase_prob = 50 + (rate_delta * 4.5) + ((wickets_left - 5) * 4.0)

            # Cap limits
            base_chase_prob = max(3.0, min(97.0, base_chase_prob))
            defend_prob = 100.0 - base_chase_prob

            st.divider()
            st.subheader("Live Win Expectancy")
            st.progress(int(base_chase_prob))
            
            st.write(f"**{chasing_team} (Chasing)**: `{round(base_chase_prob, 1)}%`")
            st.write(f"**{defending_team} (Defending)**: `{round(defend_prob, 1)}%`")

            if base_chase_prob >= 50:
                st.info(f"📈 **Match Trend:** {chasing_team} is currently favored to chase down the target with {wickets_left} wickets intact.")
            else:
                st.warning(f"📉 **Match Trend:** Required run rate ({rrr:.2f}) is putting pressure on {chasing_team}. {defending_team} is in the driver's seat.")
    
