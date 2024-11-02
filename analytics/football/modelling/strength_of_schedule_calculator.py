from statistics import mean
from typing import List, Dict

from football.league_table import LeagueTableRow, GamePOV
from football.modelling.game_chooser import GameChooser
from football.models import Team


def calculate_opponents_ranking(team: Team,
                                game_chooser: GameChooser,
                                rows_by_team: Dict[Team, LeagueTableRow],
                                team_ratings: Dict[Team, float],
                                remove_games_against: Team = None):
    if remove_games_against is None:
        games = game_chooser.choose_games(rows_by_team[team])
    else:
        games = remove_games_against_team(
            game_chooser.choose_games(rows_by_team[team]),
            remove_games_against
        )

    if len(games) == 0:
        return None

    opponent_rankings = [
        team_ratings[game_pov.opposition] * home_advantage_multiplier(game_pov)
        for game_pov in games
    ]
    return mean(opponent_rankings)

def calculate_opponents_opponents_ranking(team: Team,
                                          game_chooser: GameChooser,
                                          rows_by_team: Dict[Team, LeagueTableRow],
                                          team_ratings: Dict[Team, float]):
    opponents_opponents_rankings = [
        calculate_opponents_ranking(
            game_pov.opposition,
            game_chooser,
            rows_by_team,
            team_ratings,
            team
        )
        for game_pov in game_chooser.choose_games(rows_by_team[team])
    ]
    opponents_opponents_rankings = [r for r in opponents_opponents_rankings if r is not None]
    return mean(opponents_opponents_rankings)

def remove_games_against_team(games: List[GamePOV], team: Team):
    return [g for g in games if g.opposition != team]

def home_advantage_multiplier(game_pov: GamePOV):
    return 1.25 if not game_pov.is_home else 1.0

def calculate_strength_of_schedule(team: Team,
                                   game_chooser: GameChooser,
                                   rows_by_team: Dict[Team, LeagueTableRow],
                                   team_ratings: Dict[Team, float]):
    return ((2/3) * calculate_opponents_ranking(team, game_chooser, rows_by_team, team_ratings)
            + (1/3) * calculate_opponents_opponents_ranking(team, game_chooser, rows_by_team, team_ratings))