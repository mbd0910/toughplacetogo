from django.test import TestCase

from football.league_table import GamePOV, LeagueTableRow
from football.modelling.game_chooser import ResultsChooser
from football.modelling.strength_of_schedule_calculator import team_rating, calculate_strength_of_schedule, calculate_opponents_ranking, calculate_opponents_opponents_ranking
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

    def test_all_the_things(self):
        team_1 = Team(name='Team 1')
        team_2 = Team(name='Team 2')
        team_3 = Team(name='Team 3')
        team_4 = Team(name='Team 4')
        team_1_row = LeagueTableRow(team=team_1)
        team_2_row = LeagueTableRow(team=team_2)
        team_3_row = LeagueTableRow(team=team_3)
        team_4_row = LeagueTableRow(team=team_4)
        team_1_row.add_result(GamePOV(team_1, team_2, is_home=True, scored=1, conceded=1))
        team_2_row.add_result(GamePOV(team_2, team_1, is_home=False, scored=1, conceded=1))
        team_3_row.add_result(GamePOV(team_3, team_1, is_home=True, scored=2, conceded=1))
        team_1_row.add_result(GamePOV(team_1, team_3, is_home=False, scored=1, conceded=2))
        team_2_row.add_result(GamePOV(team_2, team_3, is_home=True, scored=0, conceded=1))
        team_3_row.add_result(GamePOV(team_3, team_2, is_home=False, scored=1, conceded=0))
        team_4_row.add_result(GamePOV(team_4, team_2, is_home=True, scored=3, conceded=4))
        team_2_row.add_result(GamePOV(team_2, team_4, is_home=False, scored=4, conceded=3))
        team_1_row.xg = 0.3
        team_1_row.xg_against = 0.2
        team_2_row.xg = 0.4
        team_2_row.xg_against = 0.2
        team_3_row.xg = 0.8
        team_3_row.xg_against = 0.3
        team_4_row.xg = 0.7
        team_4_row.xg_against = 0.8

        team_1_rating = team_rating(team_1_row)
        team_2_rating = team_rating(team_2_row)
        team_3_rating = team_rating(team_3_row)
        team_4_rating = team_rating(team_4_row)

        self.assertAlmostEqual(-0.115, team_1_rating)
        self.assertAlmostEqual(0.0467, team_2_rating, 4)
        self.assertAlmostEqual(0.475, team_3_rating)
        self.assertAlmostEqual(-0.37, team_4_rating)

        rows_by_team_name = {
            'Team 1': team_1_row,
            'Team 2': team_2_row,
            'Team 3': team_3_row,
            'Team 4': team_4_row,
        }

        team_1_opponents_ranking = calculate_opponents_ranking(
            team_1,
            ResultsChooser(),
            rows_by_team_name
        )
        team_2_opponents_ranking = calculate_opponents_ranking(
            team_2,
            ResultsChooser(),
            rows_by_team_name
        )
        team_3_opponents_ranking = calculate_opponents_ranking(
            team_3,
            ResultsChooser(),
            rows_by_team_name
        )
        team_4_opponents_ranking = calculate_opponents_ranking(
            team_4,
            ResultsChooser(),
            rows_by_team_name
        )

        self.assertAlmostEqual(0.2608, team_1_opponents_ranking, 4)
        self.assertAlmostEqual(-0.0033, team_2_opponents_ranking, 4)
        self.assertAlmostEqual(-0.0342, team_3_opponents_ranking, 4)
        self.assertAlmostEqual(0.0467, team_4_opponents_ranking, 4)

        team_1_opponents_opponents_ranking = calculate_opponents_opponents_ranking(
            team_1,
            ResultsChooser(),
            rows_by_team_name
        )
        team_2_opponents_opponents_ranking = calculate_opponents_opponents_ranking(
            team_2,
            ResultsChooser(),
            rows_by_team_name
        )
        team_3_opponents_opponents_ranking = calculate_opponents_opponents_ranking(
            team_3,
            ResultsChooser(),
            rows_by_team_name
        )
        team_4_opponents_opponents_ranking = calculate_opponents_opponents_ranking(
            team_4,
            ResultsChooser(),
            rows_by_team_name
        )

        self.assertAlmostEqual(0.0496, team_1_opponents_opponents_ranking, 4)
        self.assertAlmostEqual(0.18, team_2_opponents_opponents_ranking)
        self.assertAlmostEqual(-0.0979, team_3_opponents_opponents_ranking, 4)
        self.assertAlmostEqual(0.18, team_4_opponents_opponents_ranking, 4)

        team_1_strength_of_schedule = calculate_strength_of_schedule(team_1, ResultsChooser(), rows_by_team_name)
        team_2_strength_of_schedule = calculate_strength_of_schedule(team_2, ResultsChooser(), rows_by_team_name)
        team_3_strength_of_schedule = calculate_strength_of_schedule(team_3, ResultsChooser(), rows_by_team_name)
        team_4_strength_of_schedule = calculate_strength_of_schedule(team_4, ResultsChooser(), rows_by_team_name)

        self.assertAlmostEqual(0.1904, team_1_strength_of_schedule, 4)
        self.assertAlmostEqual(0.0578, team_2_strength_of_schedule, 4)
        self.assertAlmostEqual(-0.0554, team_3_strength_of_schedule, 4)
        self.assertAlmostEqual(0.0911, team_4_strength_of_schedule, 4)