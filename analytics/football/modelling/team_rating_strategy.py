from abc import ABC, abstractmethod
from typing import Dict

from football.league_table import LeagueTableRow
from football.models import Team

class TeamRatingStrategy(ABC):
    @abstractmethod
    def calculate_team_ratings(self, rows_by_team: Dict[Team, LeagueTableRow]) -> Dict[Team, float]:
        pass

class WeightedGoalDifferenceTeamRatingStrategy(TeamRatingStrategy):
    def __init__(self, xg_gd_weight):
        self.xg_gd_weight = xg_gd_weight

    def calculate_team_ratings(self, rows_by_team: Dict[Team, LeagueTableRow]) -> Dict[Team, float]:
        return {
            team: self.calculate_team_rating(row)
            for team, row in rows_by_team.items()
        }

    def calculate_team_rating(self, row: LeagueTableRow):
        return self.xg_gd_weight * row.xg_difference_per_game() + (1 - self.xg_gd_weight) * row.goal_difference_per_game()

class LeaguePositionTeamRatingStrategy(TeamRatingStrategy):
    def calculate_team_ratings(self, rows_by_team: Dict[Team, LeagueTableRow]) -> Dict[Team, float]:
        rows_sorted_by_performance_points = sorted(
            rows_by_team.values(),
            key=lambda row: (row.points(), row.goal_difference(), row.scored, row.xg_difference_per_game),
            reverse=True
        )

        number_of_teams = len(rows_sorted_by_performance_points)

        # In a twenty team league, we want:
        # - the team in 1st place to have a rating of 20
        # - the team in 2nd place to have a rating of 19
        # - ...
        # - the team in 20th place to have a rating of 1
        return {
            row.team: number_of_teams - index
            for index, row in enumerate(rows_sorted_by_performance_points)
        }