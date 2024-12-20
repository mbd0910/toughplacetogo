from typing import List, Dict

import numpy as np
from scipy.stats import zscore

from football.models import Team


class GamePOV:
    def __init__(self, team: Team, opposition: Team, is_home: bool, scored: int, conceded: int):
        self.team = team
        self.opposition = opposition
        self.is_home = is_home
        self.scored = scored
        self.conceded = conceded


class LeagueTableRow:
    def __init__(self, team: Team, points_deduction=0, results=None, fixtures=None, wins=0, draws=0):
        if results is None:
            results = []
        if fixtures is None:
            fixtures = []
        self.team = team
        self.points_deduction = points_deduction
        self.wins = wins
        self.draws = draws
        self.losses = 0
        self.scored = 0
        self.conceded = 0
        self.results = results
        self.fixtures = fixtures
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

    def performance_points_per_game(self):
        return self.performance_points() / len(self.results)

    def x_points_per_game(self):
        return self.x_points / len(self.results)

    def goal_difference(self):
        return self.scored - self.conceded

    def goal_difference_per_game(self):
        return float(self.goal_difference() / len(self.results))

    def xg_difference(self):
        return self.xg - self.xg_against

    def xg_difference_per_game(self):
        return float(self.xg_difference() / len(self.results))

    def result_opponents(self):
        return [game_pov.opposition.name for game_pov in self.results]

    def add_result(self, game_pov: GamePOV):
        self.results.append(game_pov)
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

    def add_fixture(self, fixture_pov: GamePOV):
        self.fixtures.append(fixture_pov)

    def most_recent_games(self, limit = 5):
        if limit <= 0:
            return []
        return self.results[-limit:]

    def upcoming_games(self, limit = 5) -> List[GamePOV]:
        if limit <= 0:
            return []
        return self.fixtures[:limit]

    def most_recent_home_games(self, limit = 5):
        return self.most_recent_games_matching_criteria(is_home=True, limit=limit)

    def most_recent_away_games(self, limit = 5):
        return self.most_recent_games_matching_criteria(is_home=False, limit=limit)

    def games_remaining(self):
        return len(self.fixtures)

    def most_recent_games_matching_criteria(self, is_home: bool, limit = 5):
        if limit <= 0:
            return []
        filtered_list = [game_pov for game_pov in self.results if game_pov.is_home == is_home]
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

def normalise_difficulties(team_to_raw_difficulty: Dict[Team, float]) -> Dict[Team, float]:
    raw_difficulties = np.array(list(team_to_raw_difficulty.values()))
    normalized_difficulties = zscore(raw_difficulties)

    return {
        team: normalized_difficulty
        for team, normalized_difficulty in zip(team_to_raw_difficulty.keys(), normalized_difficulties)
    }
