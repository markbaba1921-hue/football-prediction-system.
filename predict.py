# predict.py
import numpy as np
from scipy.stats import poisson

# Realistic team strength data for a better demo
team_strength = {
    "Manchester City": (2.5, 0.8),   # Strong attack, strong defense
    "Liverpool": (2.3, 1.0),
    "Arsenal": (2.1, 0.9),
    "Chelsea": (1.8, 1.1),
    "Manchester United": (1.7, 1.2),
    "Tottenham Hotspur": (1.9, 1.4),
    "Newcastle United": (1.8, 1.2),
    "Aston Villa": (1.7, 1.3),
    "Brighton": (1.9, 1.5),
    "West Ham": (1.5, 1.4)
}

def predict_match(home_team_name, away_team_name):
    """
    Predicts football match outcome using Poisson distribution.
    Returns: (home_win%, draw%, away_win%, most_likely_score)
    """
    try:
        if home_team_name == away_team_name:
            return 33.3, 33.3, 33.3, "1-1"

        # Get team strengths
        home_attack, home_defense = team_strength[home_team_name]
        away_attack, away_defense = team_strength[away_team_name]

        # Calculate expected goals
        home_xG = (home_attack * away_defense) * 1.6  # league avg home goals = 1.6
        away_xG = (away_attack * home_defense) * 1.2  # league avg away goals = 1.2

        # Calculate score probabilities
        max_goals = 8  # More realistic than 10
        home_probs = [poisson.pmf(i, home_xG) for i in range(max_goals)]
        away_probs = [poisson.pmf(i, away_xG) for i in range(max_goals)]

        # Initialize probabilities
        home_win_prob = 0
        draw_prob = 0
        away_win_prob = 0
        most_likely_score = ""
        max_prob = -1

        # Calculate match outcomes
        for i in range(max_goals):
            for j in range(max_goals):
                p = home_probs[i] * away_probs[j]
                if i > j:
                    home_win_prob += p
                elif i == j:
                    draw_prob += p
                else:
                    away_win_prob += p

                if p > max_prob:
                    max_prob = p
                    most_likely_score = f"{i}-{j}"

        # Convert to percentages
        return (
            round(home_win_prob * 100, 1),
            round(draw_prob * 100, 1),
            round(away_win_prob * 100, 1),
            most_likely_score
        )
    
    except Exception as e:
        # Return neutral prediction if something goes wrong
        return 33.3, 33.3, 33.3, "1-1"

def get_teams():
    """Return list of available teams"""
    return list(team_strength.keys())
