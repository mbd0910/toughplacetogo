from models import db, Team, Game, GameTeam, Competition, Season, Stage
import numpy as np
from scipy.optimize import minimize
from typing import List


def init_db():
    db.connect()
    db.create_tables([Team, Game, GameTeam, Competition, Season, Stage])


# All the games in the database
matches: List[Game] = Game.select().prefetch(GameTeam, Team)
teams = Team.select()
n_teams = len(teams)

# Create team indices
team_indices = {team: idx for idx, team in enumerate(teams)}

# print(team_indices)
# exit(0)

# Initialize parameters: attack and defense strengths, and home advantage
initial_params = np.concatenate([
    np.random.rand(n_teams),  # attack parameters
    np.random.rand(n_teams),  # defense parameters
    np.array([0.1])           # home advantage
])


def likelihood(params):
    attack_params = params[:n_teams]
    defense_params = params[n_teams:2*n_teams]
    home_adv = params[2*n_teams]

    log_likelihood = 0
    for match in matches:
        home_team = match.home_team().team
        away_team = match.away_team().team
        home_goals = match.home_team().full_time_score
        away_goals = match.away_team().full_time_score

        home_idx = team_indices[home_team]
        away_idx = team_indices[away_team]

        lambda_home = np.exp(attack_params[home_idx] - defense_params[away_idx] + home_adv)
        lambda_away = np.exp(attack_params[away_idx] - defense_params[home_idx])

        log_likelihood += (home_goals * np.log(lambda_home) - lambda_home) + (away_goals * np.log(lambda_away) - lambda_away)

    return -log_likelihood


options = {
    'disp': True,  # Display convergence messages
    'gtol': 1e-5,  # Gradient tolerance
    'ftol': 1e-5,  # Function tolerance
    'maxiter': 1000  # Maximum number of iterations
}

# Minimize the negative log-likelihood
result = minimize(likelihood, initial_params, method='L-BFGS-B', options=options)

# Extract the optimized parameters
attack_params = result.x[:n_teams]
defense_params = result.x[n_teams:2*n_teams]
home_adv = result.x[2*n_teams]

# Output the results
team_parameters = {team: (attack_params[idx], defense_params[idx]) for team, idx in team_indices.items()}

print("Team Parameters (Attack, Defense):")
for team, params in team_parameters.items():
    print(f"{team}: Attack={params[0]:.4f}, Defense={params[1]:.4f}")

print(f"Home Advantage: {home_adv:.4f}")
