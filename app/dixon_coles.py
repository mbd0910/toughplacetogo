from models import db, Team, Game, GameTeam, Competition, Season, Stage
import numpy as np
from scipy.optimize import minimize
from typing import List
from datetime import datetime


def init_db():
    db.connect()
    db.create_tables([Team, Game, GameTeam, Competition, Season, Stage])


# All the games in the database
cutoff = datetime(2021, 7, 1)

# Order these games so the oldest are first
matches: List[Game] = (Game.select()
                       .where(Game.kickoff > cutoff)
                       .order_by(Game.kickoff.asc())
                       .prefetch(GameTeam, Team))
# Only select the teams that have played in these matches
teams_to_stats = {}

for match in matches:
    home_team_result = match.home_team()
    away_team_result = match.away_team()
    home_team = home_team_result.team
    away_team = away_team_result.team

    if home_team not in teams_to_stats:
        teams_to_stats[home_team] = {
            'most_recent_competition': None,
            'scored': 0,
            'conceded': 0,
            'games': 0
        }

    if away_team not in teams_to_stats:
        teams_to_stats[away_team] = {
            'most_recent_competition': None,
            'scored': 0,
            'conceded': 0,
            'games': 0
        }

    teams_to_stats[home_team]['most_recent_competition'] = match.stage.season.competition.name
    teams_to_stats[away_team]['most_recent_competition'] = match.stage.season.competition.name

    teams_to_stats[home_team]['scored'] += home_team_result.full_time_score
    teams_to_stats[home_team]['conceded'] += away_team_result.full_time_score
    teams_to_stats[home_team]['games'] += 1

    teams_to_stats[away_team]['scored'] += away_team_result.full_time_score
    teams_to_stats[away_team]['conceded'] += home_team_result.full_time_score
    teams_to_stats[away_team]['games'] += 1

teams = teams_to_stats.keys()
n_teams = len(teams)

for team, stats in teams_to_stats.items():
    stats['avg_scored'] = stats['scored'] / stats['games']
    stats['avg_conceded'] = stats['conceded'] / stats['games']

# Create team indices
team_indices = {team: idx for idx, team in enumerate(teams)}

division_multipliers = {
    'Premier League': 1.2,
    'Championship': 1.0,
    'League One': 0.8,
    'League Two': 0.6,
    'National League': 0.4
}

initial_attack = np.zeros(n_teams)
initial_defence = np.zeros(n_teams)

for team, stats in teams_to_stats.items():
    index = team_indices[team]
    most_recent_competition = stats['most_recent_competition']
    multiplier = division_multipliers[most_recent_competition]

    initial_attack[index] = np.log(multiplier * stats['avg_scored'] + 1e-5)
    initial_defence[index] = np.log(multiplier * stats['avg_conceded'] + 1e-5)

# Initialize parameters: attack and defense strengths, and home advantage
initial_params = np.concatenate([
    initial_attack,  # attack parameters
    initial_defence,  # defense parameters
    np.array([0.1])           # home advantage
])

initial_params_no_opt = np.concatenate([
    np.random.rand(n_teams),
    np.random.rand(n_teams),
    np.array([0.1])
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
result_no_opt = minimize(likelihood, initial_params_no_opt, method='L-BFGS-B', options=options)

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

print("Parameters without initial optimization:", result_no_opt.x)
print("Parameters with initial optimization:", result.x)

# Check if the results are close
are_results_close = np.allclose(result_no_opt.x, result.x, atol=1e-5)
print("Are the final parameters close?", are_results_close)
