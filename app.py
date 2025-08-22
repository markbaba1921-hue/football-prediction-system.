# app.py
import streamlit as st
from predict import predict_match, get_teams

# Page configuration
st.set_page_config(
    page_title="Football Predictor",
    page_icon="⚽",
    layout="centered"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {font-size: 3rem; color: #1E88E5; text-align: center;}
    .subheader {font-size: 1.2rem; color: #666; text-align: center;}
    .prediction-box {background-color: #F0F2F6; padding: 20px; border-radius: 10px;}
    .score-display {font-size: 2.5rem; font-weight: bold; text-align: center; color: #FF4B4B;}
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">⚽ Football Match Predictor</h1>', unsafe_allow_html=True)
st.markdown('<p class="subheader">Predict match outcomes using Poisson distribution analysis</p>', unsafe_allow_html=True)

# Disclaimer
st.warning("⚠️ This is a demonstration app with simulated data. Not for actual betting.")

# Get available teams
try:
    teams = get_teams()
except:
    st.error("Error loading teams data")
    st.stop()

# Create selection columns
col1, col2 = st.columns(2)
with col1:
    home_team = st.selectbox("**Home Team**", teams, index=0)
with col2:
    away_team = st.selectbox("**Away Team**", teams, index=1)

# Predict button
if st.button("**Predict Match Outcome** 🚀", type="primary", use_container_width=True):
    
    with st.spinner('Analyzing team strengths and calculating probabilities...'):
        # Get prediction
        home_win, draw, away_win, score = predict_match(home_team, away_team)
    
    # Display results
    st.success("Prediction Complete!")
    
    # Match header
    st.subheader(f"{home_team} vs {away_team}")
    
    # Most likely score
    st.markdown('<div class="prediction-box">', unsafe_allow_html=True)
    st.markdown("**Most Likely Score**")
    st.markdown(f'<div class="score-display">{score}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Probabilities
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Home Win", f"{home_win}%", delta=f"{home_win-33.3:+.1f}%")
    with col2:
        st.metric("Draw", f"{draw}%", delta=f"{draw-33.3:+.1f}%")
    with col3:
        st.metric("Away Win", f"{away_win}%", delta=f"{away_win-33.3:+.1f}%")
    
    # Probability chart
    chart_data = {
        'Outcome': ['Home Win', 'Draw', 'Away Win'],
        'Probability': [home_win, draw, away_win]
    }
    st.bar_chart(chart_data, x='Outcome', y='Probability', color="#FF4B4B")

# Footer
st.markdown("---")
st.caption("Built with Streamlit • Poisson Distribution Model • Demo Version")
