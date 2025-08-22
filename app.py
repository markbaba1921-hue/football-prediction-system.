import streamlit as st
import joblib

# Load model
model = joblib.load("football_model.pkl")

st.title("⚽ Football Match Prediction System")

st.write("Enter estimated goals for home and away teams:")

home_goals = st.number_input("Home Team Goals", min_value=0, max_value=10, step=1)
away_goals = st.number_input("Away Team Goals", min_value=0, max_value=10, step=1)

if st.button("Predict Outcome"):
    prediction = model.predict([[home_goals, away_goals]])[0]

    if prediction == 1:
        st.success("🏆 Home team likely to win!")
    elif prediction == -1:
        st.success("⚽ Away team likely to win!")
    else:
        st.success("🤝 Likely a draw!")
