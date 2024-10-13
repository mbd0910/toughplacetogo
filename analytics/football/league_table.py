from football.models import Team
from typing import List, Dict
from statistics import mean
import numpy as np
from scipy.stats import zscore

class GamePOV:
    def __init__(self, team: Team, opposition: Team, scored: int, conceded: int, is_home: bool):
        self.team = team
        self.opposition = opposition
        self.scored = scored
        self.conceded = conceded
        self.is_home = is_home


class LeagueTableRow:
    def __init__(self, team: Team, points_deduction=0, game_povs=None, wins=0, draws=0):
        if game_povs is None:
            game_povs = []
        self.team = team
        self.points_deduction = points_deduction
        self.wins = wins
        self.draws = draws
        self.losses = 0
        self.scored = 0
        self.conceded = 0
        self.game_povs = game_povs
        self.xg = 0
        self.xg_against = 0
        self.x_points = 0

    def games_played(self):
        return self.wins + self.draws + self.losses

    def points(self):
        return self.performance_points() - self.points_deduction

    def has_points_deducted(self):
        return self.points_deduction > 0

    def performance_points(self):
        return 3 * self.wins + self.draws

    def goal_difference(self):
        return self.scored - self.conceded

    def xg_difference(self):
        return self.xg - self.xg_against

    def add_game_pov(self, game_pov: GamePOV):
        self.game_povs.append(game_pov)
        goals_scored = game_pov.scored
        goals_conceded = game_pov.conceded
        self.scored += goals_scored
        self.conceded += goals_conceded

        if goals_scored > goals_conceded:
            self.wins += 1
        elif goals_scored == goals_conceded:
            self.draws += 1
        else:
            self.losses += 1

    def most_recent_games(self, limit = 5):
        if limit <= 0:
            return []
        return self.game_povs[-limit:]

    def most_recent_home_games(self, limit = 5):
        return self.most_recent_games_matching_criteria(is_home=True, limit=limit)

    def most_recent_away_games(self, limit = 5):
        return self.most_recent_games_matching_criteria(is_home=False, limit=limit)

    def most_recent_games_matching_criteria(self, is_home: bool, limit = 5):
        if limit <= 0:
            return []
        filtered_list = [game_pov for game_pov in self.game_povs if game_pov.is_home == is_home]
        return filtered_list[-limit:]

    def __str__(self):
        return f"{self.team.name} {self.games_played()} {self.wins} {self.draws} {self.losses} {self.scored} {self.conceded} {self.points()}"


class LeagueTable:
    def __init__(self, sorted_rows: List[LeagueTableRow]):
        self.sorted_rows = sorted_rows

    def team_to_position(self):
        return {row.team: position for position, row in enumerate(self.sorted_rows, start=1)}

    def __str__(self):
        return "\n".join(row.__str__() for row in self.sorted_rows)


def calculate_fixture_difficulty(row: LeagueTableRow, team_to_position: Dict[Team, int]):
    team_position = team_to_position[row.team]
    positions = [
        team_to_position[game_pov.opposition] - 1 if team_to_position[game_pov.opposition] > team_position else team_to_position[game_pov.opposition]
        for game_pov in row.game_povs
    ]
    return mean(positions) if positions else None

def calculate_fixture_difficulties(league_table: LeagueTable) -> Dict[Team, float]:
    team_to_position = league_table.team_to_position()
    raw_league_position_fixture_difficulties = \
        {row.team: calculate_fixture_difficulty(row, team_to_position) for row in league_table.sorted_rows}

    return raw_league_position_fixture_difficulties

def normalise_fixture_difficulties(team_to_raw_difficulty: Dict[Team, float]) -> Dict[Team, float]:
    raw_difficulties = np.array(list(team_to_raw_difficulty.values()))
    normalized_difficulties = zscore(raw_difficulties)

    return {
        team: normalized_difficulty
        for team, normalized_difficulty in zip(team_to_raw_difficulty.keys(), normalized_difficulties)
    }

def weight_fixture_difficulties(league_position_weight: float, league_position_difficulties: Dict[Team, float],
                                x_points_position_weight: float, x_points_position_difficulties: Dict[Team, float]):
    return {
        team: league_position_weight * weight + x_points_position_weight * x_points_position_difficulties.get(team)
        for team, weight in league_position_difficulties.items()
    }

