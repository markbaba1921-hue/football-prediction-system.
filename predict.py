# predict.py
import numpy as np
from scipy.stats import poisson

# 1. Define our data: Team Attack and Defense Strength
# This is HARDCODED for this demo. In a real app, you would calculate these values
# from a large historical dataset or fetch them from an API.
# Format: {Team_Name: (Attack_Strength, Defense_Strength)}
team_strength = {
    "Manchester City": (2.5, 0.8),   # Very strong attack, very strong defense
    "Liverpool": (2.3, 1.0),
    "Arsenal": (2.1, 0.9),
    "Chelsea": (1.8, 1.1),
    "Manchester United": (1.7, 1.2),
    "Tottenham Hotspur": (1.9, 1.4), # Good attack, weaker defense
}

# 2. The core prediction function
def predict_match(home_team_name, away_team_name):
    """
    Predicts the outcome of a match between home and away team using Poisson distribution.
    Returns predicted probabilities for home win, draw, away win, and the most likely score.
    """

    # Check if the same team is selected
    if home_team_name == away_team_name:
        return 0.0, 1.0, 0.0, "0-0" # Return a draw

    # Get the pre-defined strength for the selected teams
    home_attack, home_defense = team_strength[home_team_name]
    away_attack, away_defense = team_strength[away_team_name]

    # 3. Calculate Lambda (λ) - the expected goals for each team
    # We assume a "league average" of 1.6 goals per game at home and 1.2 away.
    # This is a simplification. Real models calculate this from data.
    league_avg_home_goals = 1.6
    league_avg_away_goals = 1.2

    # Expected Goals for Home Team = Home_Attack * Away_Defense * League_Avg_Home
    home_expected_goals = (home_attack * away_defense) * league_avg_home_goals
    # Expected Goals for Away Team = Away_Attack * Home_Defense * League_Avg_Away
    away_expected_goals = (away_attack * home_defense) * league_avg_away_goals

    # 4. Use Poisson distribution to calculate probability of each possible scoreline
    # We'll consider possibilities from 0 to 10 goals for each team.
    max_goals = 10
    home_probs = [poisson.pmf(i, home_expected_goals) for i in range(max_goals)]
    away_probs = [poisson.pmf(i, away_expected_goals) for i in range(max_goals)]

    # Initialize counters for our probabilities
    prob_home_win = 0.0
    prob_draw = 0.0
    prob_away_win = 0.0

    # Initialize variables to find the most likely score
    most_likely_score = ""
    max_probability = -1

    # Loop through every possible scoreline (e.g., 0-0, 5-3, 2-1)
    for home_goals in range(max_goals):
        for away_goals in range(max_goals):
            # Probability of this exact scoreline is P(Home Scores X) * P(Away Scores Y)
            score_probability = home_probs[home_goals] * away_probs[away_goals]

            # Add this probability to the correct outcome bucket
            if home_goals > away_goals:
                prob_home_win += score_probability
            elif home_goals == away_goals:
                prob_draw += score_probability
            else:
                prob_away_win += score_probability

            # Check if this is the most likely score we've seen so far
            if score_probability > max_probability:
                max_probability = score_probability
                most_likely_score = f"{home_goals}-{away_goals}"

    # 5. Return the probabilities as percentages and the most likely score
    return (prob_home_win * 100, prob_draw * 100, prob_away_win * 100, most_likely_score)

# This list of teams is imported by app.py to populate the dropdown menus
def get_teams():
    return list(team_strength.keys())
