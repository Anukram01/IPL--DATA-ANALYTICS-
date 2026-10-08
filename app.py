import streamlit as st
import pandas as pd
import joblib

st.set_page_config(page_title="IPL Match Predictor", layout="centered")

# Pre-trained models load karein
pipeline = joblib.load('ipl_winner_model.pkl')
meta = joblib.load('model_meta.pkl')

st.title("🏏 IPL Match Outcome Predictor")
st.markdown("Predict match win probabilities using historical data.")

team1 = st.selectbox("Select Team 1", meta['teams'])
avail_team2 = [t for t in meta['teams'] if t != team1]
team2 = st.selectbox("Select Team 2", avail_team2)
venue = st.selectbox("Select Venue", meta['venues'])

col1, col2 = st.columns(2)
with col1:
    toss_winner = st.selectbox("Toss Winner", [team1, team2])
with col2:
    toss_decision = st.selectbox("Toss Decision", ['bat', 'field'])

if st.button("Predict Win Probability", type="primary"):
    input_data = pd.DataFrame({
        'team1': [team1],
        'team2': [team2],
        'venue': [venue],
        'toss_winner': [toss_winner],
        'toss_decision': [toss_decision]
    })
    probs = pipeline.predict_proba(input_data)[0]
    st.divider()
    st.subheader(f"🏆 {team1} Win Chance: {round(probs[1]*100, 1)}%")
    st.subheader(f"🏆 {team2} Win Chance: {round(probs[0]*100, 1)}%")
