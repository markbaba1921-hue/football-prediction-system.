# app.py
import streamlit as st
from predict import predict_match, get_teams

# --- PAGE CONFIGURATION ---
# Set the tab title and icon
st.set_page_config(page_title="Football Predictor", page_icon="⚽", layout="centered")

# --- TITLE AND DESCRIPTION ---
st.title("⚽ Football Match Predictor")
st.markdown("""
This app predicts the outcome of a football match using a **Poisson Distribution** model.
Select the **home** and **away** teams below and click **Predict**!
""")
# A little warning that it's a demo
st.info("ℹ️ This is a demo with a limited set of teams and hardcoded data for illustration.")

# --- GET THE LIST OF TEAMS ---
available_teams = get_teams()

# --- USER INPUT FORM ---
# Using a form makes the UI cleaner
with st.form("prediction_form"):
    # Create two columns for the dropdowns
    col1, col2 = st.columns(2)
    with col1:
        home_team = st.selectbox("Home Team", available_teams, index=0) # index=0 selects the first team by default
    with col2:
        # index=1 selects the second team (Liverpool) by default for a quick demo
        away_team = st.selectbox("Away Team", available_teams, index=1)
    # The button to submit the form and start the prediction
    predict_button = st.form_submit_button("Predict Outcome! 🚀")

# --- CALCULATE AND DISPLAY PREDICTION ---
# This block only runs after the user clicks the button
if predict_button:
    # Show a spinner while calculating to let the user know something is happening
    with st.spinner('Crunching the numbers...'):
        # Call our function from predict.py
        home_win_p, draw_p, away_win_p, likely_score = predict_match(home_team, away_team)

    # --- DISPLAY THE RESULTS ---
    st.success("Prediction Complete!")
    st.subheader(f"**{home_team}** vs **{away_team}**")

    # Show the most likely score in a big font
    st.metric(label="**Most Likely Score**", value=likely_score)

    # Create three columns to show the probabilities nicely side-by-side
    col1, col2, col3 = st.columns(3)
    with col1:
        # :.1f means format the number to 1 decimal place
        st.metric(label="Home Win", value=f"{home_win_p:.1f}%")
    with col2:
        st.metric(label="Draw", value=f"{draw_p:.1f}%")
    with col3:
        st.metric(label="Away Win", value=f"{away_win_p:.1f}%")

    # Create a simple bar chart for visual learners
    st.subheader("Probability Breakdown")
    # We need to put the data in a format Streamlit's bar chart understands
    chart_data = {
        'Outcome': ['Home Win', 'Draw', 'Away Win'],
        'Probability (%)': [home_win_p, draw_p, away_win_p]
    }
    st.bar_chart(chart_data, x='Outcome', y='Probability (%)', color="#FF4B4B") # Streamlit's red color

# --- FOOTER ---
st.markdown("---")
st.caption("Built with Streamlit. Model based on Poisson distribution. | This is a simulation for demonstration purposes.")
