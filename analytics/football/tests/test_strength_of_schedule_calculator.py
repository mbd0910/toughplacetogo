from django.test import TestCase

from football.league_table import GamePOV, LeagueTableRow
from football.modelling.strength_of_schedule_calculator import team_rating
from football.models import Team


class StrengthOfScheduleCalculatorTestCase(TestCase):
    def test_team_rating(self):
        charlton = Team(name='Charlton')
        league_table_row = LeagueTableRow(charlton)
        league_table_row.xg = 4.40
        league_table_row.xg_against = 3.63

        opposition1 = Team(name='Opposition 1')
        opposition2 = Team(name='Opposition 2')
        opposition3 = Team(name='Opposition 3')
        league_table_row.add_result(GamePOV(charlton, opposition1, scored=3, conceded=0, is_home=True))
        league_table_row.add_result(GamePOV(charlton, opposition2, scored=2, conceded=1, is_home=False))
        league_table_row.add_result(GamePOV(charlton, opposition3, scored=1, conceded=0, is_home=True))

        # Total scored = 3 + 2 + 1 = 6
        # Total concede = 1
        # GD = 5
        # GD / game = 5/3
        # xg difference = 4.4 - 3.63 = 0.77
        # xg difference / game = 0.77/3
        # Team rating = 0.7 * 0.77/3 + 0.3 * 5/3 ~= 0.680 (3dp)
        self.assertAlmostEqual(0.680, team_rating(league_table_row), 3)
