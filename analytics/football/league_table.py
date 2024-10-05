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
    def __init__(self, team: Team, game_povs=None):
        if game_povs is None:
            game_povs = []
        self.team = team
        self.wins = 0
        self.draws = 0
        self.losses = 0
        self.scored = 0
        self.conceded = 0
        self.game_povs = game_povs

    def games_played(self):
        return self.wins + self.draws + self.losses

    def points(self):
        return 3 * self.wins + self.draws

    def goal_difference(self):
        return self.scored - self.conceded

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


class FixtureDifficulty:
    def __init__(self, average_position):
        self.average_position = average_position

    def __str__(self):
        return f'Average position of opponent is {self.average_position}'

def calculate_fixture_difficulty(row: LeagueTableRow, team_to_position: Dict[Team, int]):
    team_position = team_to_position[row.team]
    positions = [
        team_to_position[game_pov.opposition] - 1 if team_to_position[game_pov.opposition] > team_position else team_to_position[game_pov.opposition]
        for game_pov in row.game_povs
    ]
    return mean(positions) if positions else None

def calculate_fixture_difficulties(league_table: LeagueTable) -> Dict[LeagueTableRow, float]:
    team_to_position = league_table.team_to_position()
    raw_league_position_fixture_difficulties = \
        {row: calculate_fixture_difficulty(row, team_to_position) for row in league_table.sorted_rows}

    return raw_league_position_fixture_difficulties

def normalise_fixture_difficulties(row_to_raw_difficulty: Dict[LeagueTableRow, float]) -> Dict[LeagueTableRow, float]:
    raw_difficulties = np.array(list(row_to_raw_difficulty.values()))
    normalized_difficulties = zscore(raw_difficulties)

    return {
        row: normalized_difficulty
        for row, normalized_difficulty in zip(row_to_raw_difficulty.keys(), normalized_difficulties)
    }