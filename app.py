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
    with col_t2:
        remaining_teams = [t for t in teams if t != team1]
        team2 = st.selectbox("Select Team 2", remaining_teams, index=remaining_teams.index("Chennai Super Kings") if "Chennai Super Kings" in remaining_teams else 0, key="pm_t2")

    venue = st.selectbox("Select Venue", list(venues_data.keys()), key="pm_venue")

    v_info = venues_data[venue]
    vc1, vc2, vc3 = st.columns(3)
    vc1.metric("Avg 1st Innings Score", str(v_info["avg_score"]) + " runs")
    vc2.metric("Chasing Win Rate", str(v_info["chase_win_pct"]))
    vc3.metric("Venue Strategy", "Chase & Field" if v_info["bias"] == "chase" else "Defend & Bat")

    c_toss1, c_toss2 = st.columns(2)
    with c_toss1:
        toss_winner = st.selectbox("Toss Winner", [team1, team2], key="pm_toss_win")
    with c_toss2:
        toss_decision = st.selectbox("Toss Decision", ['bat', 'field'], key="pm_toss_dec")

    if toss_decision == 'bat':
        batting_first = toss_winner
    else:
        batting_first = team2 if toss_winner == team1 else team1

    base_par = v_info["avg_score"]
    bat_factor = (team_strengths[batting_first]["batting"] - 8.5) * 12
    proj_min = int(base_par + bat_factor - 7)
    proj_max = int(base_par + bat_factor + 8)
    pp_min = int(proj_min * 0.28)
    pp_max = int(proj_max * 0.31)

    st.info("🎯 Projected 1st Innings: " + str(proj_min) + " - " + str(proj_max) + " runs (" + str(batting_first) + " Batting 1st) | Powerplay: " + str(pp_min) + " - " + str(pp_max) + " runs")

    with st.expander("⭐ Select In-Form Impact Players (Live Form Factor)"):
        pcol1, pcol2 = st.columns(2)
        with pcol1:
            st.markdown("**" + str(team1) + " Stars**")
            selected_p1 = [p for p in team_key_players.get(team1, []) if st.checkbox(p, value=True, key="t1_star_" + str(p))]
        with pcol2:
            st.markdown("**" + str(team2) + " Stars**")
            selected_p2 = [p for p in team_key_players.get(team2, []) if st.checkbox(p, value=True, key="t2_star_" + str(p))]

    st.write("")
    if st.button("Predict Match Outcome", type="primary", use_container_width=True, key="pm_btn"):
        r1 = team_strengths[team1]["base"]
        r2 = team_strengths[team2]["base"]

        if toss_winner == team1:
            r1 *= 1.04
        else:
            r2 *= 1.04

        if (v_info["bias"] == "chase" and toss_decision == "field") or (v_info["bias"] == "defend" and toss_decision == "bat"):
            if toss_winner == team1:
                r1 *= 1.04
            else:
                r2 *= 1.04

        r1 *= (1 + (len(selected_p1) * 0.03))
        r2 *= (1 + (len(selected_p2) * 0.03))

        p1 = (r1 / (r1 + r2)) * 100
        p2 = 100 - p1

        st.divider()
        st.subheader("Match Outcome Probability")
        st.progress(int(p1))
        
        st.write("**" + str(team1) + "**: `" + str(round(p1, 1)) + "%` (Active Stars: " + str(len(selected_p1)) + ")")
        st.write("**" + str(team2) + "**: `" + str(round(p2, 1)) + "%` (Active Stars: " + str(len(selected_p2)) + ")")

        favored = team1 if p1 > p2 else team2
        st.success("🏆 Favored Winner: **" + str(favored) + "**")

        st.subheader("📊 Squad Index Comparison")
        comp_df = pd.DataFrame({
            "Metric": ["Batting Index (/10)", "Bowling Index (/10)", "Win Likelihood %"],
            team1: [team_strengths[team1]["batting"], team_strengths[team1]["bowling"], round(p1, 1)],
            team2: [team_strengths[team2]["batting"], team_strengths[team2]["bowling"], round(p2, 1)]
        }).set_index("Metric")
        st.bar_chart(comp_df)

        report_text = "=== IPL MATCH INTELLIGENCE REPORT ===\n" + \
                      "Matchup: " + str(team1) + " vs " + str(team2) + "\n" + \
                      "Venue: " + str(venue) + "\n" + \
                      "Projected Range: " + str(proj_min) + " - " + str(proj_max) + " runs\n" + \
                      "Toss Winner: " + str(toss_winner) + " (" + str(toss_decision) + ")\n" + \
                      "Probability " + str(team1) + ": " + str(round(p1, 1)) + "%\n" + \
                      "Probability " + str(team2) + ": " + str(round(p2, 1)) + "%\n" + \
                      "Favored: " + str(favored) + "\n" + \
                      "======================================"

        st.download_button(
            label="📥 Download Match Intelligence Report",
            data=report_text,
            file_name="IPL_Match_Report.txt",
            mime="text/plain",
            use_container_width=True
        )

# ================= TAB 2: LIVE CHASE & DLS SIMULATOR =================
with tab2:
    st.subheader("⚡ 2nd Innings Real-Time Chase & DLS Calculator")
    st.caption("Calculate live win chance under current overs, wickets, run rate pressure, and rain revisions.")

    sim_c1, sim_c2 = st.columns(2)
    with sim_c1:
        chasing_team = st.selectbox("Chasing Team (Batting 2nd)", teams, index=teams.index("Royal Challengers Bengaluru"), key="live_chasing")
    with sim_c2:
        defending_team = st.selectbox("Defending Team (Bowling 2nd)", [t for t in teams if t != chasing_team], index=0, key="live_defending")

    is_dls = st.checkbox("🌧️ Match Interrupted by Rain? (DLS / Revised Overs)", value=False)
    
    total_match_overs = 20.0
    if is_dls:
        total_match_overs = st.slider("Revised Total Inning Overs (DLS)", min_value=5.0, max_value=19.0, value=14.0, step=1.0)
        st.warning("⚠️ DLS Rule Active: Innings reduced to " + str(int(total_match_overs)) + " overs.")

    sc1, sc2, sc3, sc4 = st.columns(4)
    with sc1:
        raw_target = st.number_input("Original Target (20 Overs)", min_value=50, max_value=300, value=185, step=1)
    with sc2:
        current_score = st.number_input("Current Runs Scored", min_value=0, max_value=300, value=98, step=1)
    with sc3:
        wickets_down = st.number_input("Wickets Fallen", min_value=0, max_value=9, value=2, step=1)
    with sc4:
        overs_done = st.number_input("Overs Completed", min_value=1.0, max_value=float(total_match_overs - 0.1), value=min(10.0, float(total_match_overs - 1.0)), step=0.1)

    if is_dls:
        target = int(raw_target * (total_match_overs / 20.0) * 1.06)
    else:
        target = raw_target

    total_balls = int(total_match_overs * 6)
    legal_balls = int(overs_done) * 6 + int(round((overs_done - int(overs_done)) * 10))
    balls_left = max(1, total_balls - legal_balls)
    runs_needed = max(0, target - current_score)
    wickets_left = 10 - wickets_down

    crr = current_score / (legal_balls / 6) if legal_balls > 0 else 0
    rrr = runs_needed / (balls_left / 6) if balls_left > 0 else 0

    mc1, mc2, mc3, mc4 = st.columns(4)
    mc1.metric("Effective Target", str(target) + " runs" if not is_dls else str(target) + " (DLS)")
    mc2.metric("Runs Needed", runs_needed)
    mc3.metric("Balls Remaining", balls_left)
    mc4.metric("Required Rate (RRR)", f"{rrr:.2f}")

    if st.button("Calculate Live Situation Odds", type="primary", use_container_width=True, key="live_calc_btn"):
        if runs_needed <= 0:
            st.success("🎉 " + str(chasing_team) + " has reached the target and won the match!")
        else:
            rate_delta = crr - rrr
            base_chase_prob = 50 + (rate_delta * 4.5) + ((wickets_left - 5) * 4.0)

            if is_dls and wickets_left >= 7:
                base_chase_prob += 6.0

            base_chase_prob = max(3.0, min(97.0, base_chase_prob))
            defend_prob = 100.0 - base_chase_prob

            st.divider()
            st.subheader("Live Win Expectancy")
            st.progress(int(base_chase_prob))
            
            st.write("**" + str(chasing_team) + " (Chasing)**: `" + str(round(base_chase_prob, 1)) + "%`")
            st.write("**" + str(defending_team) + " (Defending)**: `" + str(round(defend_prob, 1)) + "%`")

            if base_chase_prob >= 50:
                st.info("📈 **Match Trend:** " + str(chasing_team) + " is favored to complete the chase with " + str(wickets_left) + " wickets remaining.")
            else:
                st.warning("📉 **Match Trend:** Required run rate (" + f"{rrr:.2f}" + ") is escalating. " + str(defending_team) + " holds the upper hand.")

# ================= TAB 3: RECORDS EXPLORER =================
with tab3:
    st.subheader("📚 Historical Franchise Legacy & Records Explorer")
    st.caption("Compare career tournament statistics, championship titles, and historical extreme scores.")

    r_col1, r_col2 = st.columns(2)
    with r_col1:
        hist_t1 = st.selectbox("Franchise 1", teams, index=teams.index("Royal Challengers Bengaluru"), key="hist_t1")
    with r_col2:
        hist_t2 = st.selectbox("Franchise 2", [t for t in teams if t != hist_t1], index=0, key="hist_t2")

    t1_p = team_profiles[hist_t1]
    t2_p = team_profiles[hist_t2]

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Titles Won", str(t1_p['titles']) + " vs " + str(t2_p['titles']))
    m2.metric("Finals Reached", str(t1_p['finals']) + " vs " + str(t2_p['finals']))
    m3.metric("Career Win Rate", str(t1_p['win_pct']) + "% vs " + str(t2_p['win_pct']) + "%")
    m4.metric("Highest Total", str(t1_p['highest']) + " vs " + str(t2_p['highest']))

    st.write("")
    records_df = pd.DataFrame({
        "Metric": ["IPL Titles 🏆", "Finals Appearances", "Historical Win %", "Highest Team Score", "Lowest Team Score"],
        hist_t1: [t1_p["titles"], t1_p["finals"], str(t1_p['win_pct']) + "%", t1_p["highest"], t1_p["lowest"]],
        hist_t2: [t2_p["titles"], t2_p["finals"], str(t2_p['win_pct']) + "%", t2_p["highest"], t2_p["lowest"]]
    }).set_index("Metric")

    st.table(records_df)
