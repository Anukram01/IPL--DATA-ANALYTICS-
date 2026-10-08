import streamlit as st
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestClassifier

st.set_page_config(page_title="IPL Match Predictor", page_icon="🏏", layout="centered")

@st.cache_resource
def load_and_train():
    DATA_URL = "https://raw.githubusercontent.com/Anukram01/IPL--DATA-ANALYTICS-/main/IPL_Data_Analysis.ipynb"
    # Direct raw match dataset link
    dataset_url = "https://raw.githubusercontent.com/Anukram01/IPL--DATA-ANALYTICS-/main/queries.sql"
    
    # Kaggle verified IPL dataset mirror
    csv_url = "https://raw.githubusercontent.com/sahil-sharma2109/IPL-Data-Analysis/master/matches.csv"
    df = pd.read_csv(csv_url)
    
    # Team standardization
    team_mappings = {
        "Rising Pune Supergiant": "Rising Pune Supergiants",
        "Delhi Daredevils": "Delhi Capitals",
        "Deccan Chargers": "Sunrisers Hyderabad",
        "Kings XI Punjab": "Punjab Kings",
        "Royal Challengers Bangalore": "Royal Challengers Bengaluru"
    }
    for col in ['team1', 'team2', 'winner', 'toss_winner']:
        if col in df.columns:
            df[col] = df[col].replace(team_mappings)
            
    df = df.dropna(subset=['team1', 'team2', 'venue', 'toss_winner', 'toss_decision', 'winner'])
    df['team1_win'] = (df['team1'] == df['winner']).astype(int)
    
    features = ['team1', 'team2', 'venue', 'toss_winner', 'toss_decision']
    preprocessor = ColumnTransformer([
        ('cat', OneHotEncoder(sparse_output=False, handle_unknown='ignore'), features)
    ])
    
    pipeline = Pipeline([
        ('preprocessor', preprocessor),
        ('classifier', RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42))
    ])
    
    pipeline.fit(df[features], df['team1_win'])
    
    teams = sorted(list(set(df['team1'].unique()) | set(df['team2'].unique())))
    venues = sorted(list(df['venue'].unique()))
    
    return pipeline, teams, venues

with st.spinner("Initializing Prediction Engine..."):
    pipeline, teams, venues = load_and_train()

st.title("🏏 IPL Match Outcome Predictor")
st.markdown("Predict match win probabilities using historical IPL dynamics.")

team1 = st.selectbox("Select Team 1", teams)
avail_teams = [t for t in teams if t != team1]
team2 = st.selectbox("Select Team 2", avail_teams)
venue = st.selectbox("Select Venue", venues)

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
    
