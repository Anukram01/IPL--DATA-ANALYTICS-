import streamlit as st

st.set_page_config(page_title="IPL Match Predictor", page_icon="🏏", layout="centered")

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

venues = [
    "Wankhede Stadium, Mumbai",
    "M Chinnaswamy Stadium, Bengaluru",
    "MA Chidambaram Stadium, Chepauk, Chennai",
    "Eden Gardens, Kolkata",
    "Narendra Modi Stadium, Ahmedabad",
    "Arun Jaitley Stadium, Delhi",
    "Rajiv Gandhi International Stadium, Hyderabad",
    "Punjab Cricket Association IS Bindra Stadium, Mohali"
]

base_ratings = {
    "Chennai Super Kings": 1.25,
    "Mumbai Indians": 1.22,
    "Kolkata Knight Riders": 1.16,
    "Gujarat Titans": 1.15,
    "Royal Challengers Bengaluru": 1.14,
    "Rajasthan Royals": 1.10,
    "Sunrisers Hyderabad": 1.08,
    "Lucknow Super Giants": 1.05,
    "Delhi Capitals": 0.98,
    "Punjab Kings": 0.92
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

st.title("🏏 IPL Outcome Predictor")
st.caption("Predict match win probabilities based on team strength, toss, and active player form.")

team1 = st.selectbox("Select Team 1", teams, index=teams.index("Royal Challengers Bengaluru"))

remaining_teams = [t for t in teams if t != team1]
team2 = st.selectbox("Select Team 2", remaining_teams, index=remaining_teams.index("Chennai Super Kings") if "Chennai Super Kings" in remaining_teams else 0)

venue = st.selectbox("Select Venue", venues)

toss_winner = st.selectbox("Toss Winner", [team1, team2])
toss_decision = st.selectbox("Toss Decision", ['bat', 'field'])

# Dynamic Player Form Impact Section
with st.expander("⭐ Select In-Form Impact Players (Affects Probability)"):
    st.write("Jin players ko aap select karenge, unka positive impact team ke winning chances badhayega:")
    col_p1, col_p2 = st.columns(2)
    
    with col_p1:
        st.markdown(f"**{team1} Stars**")
        selected_p1 = [p for p in team_key_players.get(team1, []) if st.checkbox(p, value=True, key=f"t1_{p}")]
        
    with col_p2:
        st.markdown(f"**{team2} Stars**")
        selected_p2 = [p for p in team_key_players.get(team2, []) if st.checkbox(p, value=True, key=f"t2_{p}")]

st.write("")

if st.button("Predict Win Probability", type="primary", use_container_width=True):
    r1 = base_ratings.get(team1, 1.0)
    r2 = base_ratings.get(team2, 1.0)

    # 1. Toss Impact (+5% advantage)
    if toss_winner == team1:
        r1 *= 1.05
    else:
        r2 *= 1.05

    # 2. Player Form Impact (Har active star player team rating me +3% add karega)
    player_boost_1 = 1 + (len(selected_p1) * 0.03)
    player_boost_2 = 1 + (len(selected_p2) * 0.03)
    
    r1 *= player_boost_1
    r2 *= player_boost_2

    p1 = (r1 / (r1 + r2)) * 100
    p2 = 100 - p1

    st.divider()
    st.subheader("Match Outcome Probability")
    st.progress(int(p1))
    
    st.write(f"**{team1}**: `{round(p1, 1)}%` (Active Impact Players: {len(selected_p1)})")
    st.write(f"**{team2}**: `{round(p2, 1)}%` (Active Impact Players: {len(selected_p2)})")

    if p1 > p2:
        st.success(f"🏆 Predicted Winner: **{team1}**")
    else:
        st.success(f"🏆 Predicted Winner: **{team2}**")
        
