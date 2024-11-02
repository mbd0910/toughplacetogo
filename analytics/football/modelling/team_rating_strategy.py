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