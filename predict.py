import joblib
import sys

# Load the trained model
model = joblib.load("football_model.pkl")

# Example usage:
# python predict.py 2 1
# (where 2 = home team goals estimate, 1 = away team goals estimate)

if len(sys.argv) != 3:
    print("Usage: python predict.py <home_goals> <away_goals>")
    sys.exit(1)

home_goals = int(sys.argv[1])
away_goals = int(sys.argv[2])

prediction = model.predict([[home_goals, away_goals]])[0]

if prediction == 1:
    print("🏆 Home team likely to win!")
elif prediction == -1:
    print("⚽ Away team likely to win!")
else:
    print("🤝 Likely a draw!")
