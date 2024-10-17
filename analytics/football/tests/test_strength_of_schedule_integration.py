from django.test import TestCase

from football.league_table import GamePOV, LeagueTableRow
from football.modelling.game_chooser import ResultsChooser
from football.modelling.strength_of_schedule_calculator import team_rating, calculate_strength_of_schedule, \
    calculate_opponents_ranking, calculate_opponents_opponents_ranking
from football.models import Team


class StrengthOfScheduleIntegrationTestCase(TestCase):
    team_1 = Team(id=1, name='Team 1')
    team_2 = Team(id=2, name='Team 2')
    team_3 = Team(id=3, name='Team 3')
    team_4 = Team(id=4, name='Team 4')
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

    rows_by_team = {
        team_1: team_1_row,
        team_2: team_2_row,
        team_3: team_3_row,
        team_4: team_4_row,
    }

    results_chooser = ResultsChooser()

    def test_team_ratings(self):
        team_1_rating = team_rating(self.team_1_row)
        team_2_rating = team_rating(self.team_2_row)
        team_3_rating = team_rating(self.team_3_row)
        team_4_rating = team_rating(self.team_4_row)

        self.assertAlmostEqual(-0.115, team_1_rating)
        self.assertAlmostEqual(0.0467, team_2_rating, 4)
        self.assertAlmostEqual(0.475, team_3_rating)
        self.assertAlmostEqual(-0.37, team_4_rating)

    def test_opponents_rankings(self):
        team_1_opponents_ranking = calculate_opponents_ranking(
            self.team_1,
            self.results_chooser,
            self.rows_by_team
        )
        team_2_opponents_ranking = calculate_opponents_ranking(
            self.team_2,
            self.results_chooser,
            self.rows_by_team
        )
        team_3_opponents_ranking = calculate_opponents_ranking(
            self.team_3,
            self.results_chooser,
            self.rows_by_team
        )
        team_4_opponents_ranking = calculate_opponents_ranking(
            self.team_4,
            self.results_chooser,
            self.rows_by_team
        )

        self.assertAlmostEqual(0.3202, team_1_opponents_ranking, 4)
        self.assertAlmostEqual(-0.0438, team_2_opponents_ranking, 4)
        self.assertAlmostEqual(-0.0283, team_3_opponents_ranking, 4)
        self.assertAlmostEqual(0.0467, team_4_opponents_ranking, 4)

    def test_opponents_opponents_rankings(self):
        team_1_opponents_opponents_ranking = calculate_opponents_opponents_ranking(
            self.team_1,
            self.results_chooser,
            self.rows_by_team
        )
        team_2_opponents_opponents_ranking = calculate_opponents_opponents_ranking(
            self.team_2,
            self.results_chooser,
            self.rows_by_team
        )
        team_3_opponents_opponents_ranking = calculate_opponents_opponents_ranking(
            self.team_3,
            self.results_chooser,
            self.rows_by_team
        )
        team_4_opponents_opponents_ranking = calculate_opponents_opponents_ranking(
            self.team_4,
            self.results_chooser,
            self.rows_by_team
        )

        self.assertAlmostEqual(0.0323, team_1_opponents_opponents_ranking, 4)
        self.assertAlmostEqual(0.2394, team_2_opponents_opponents_ranking, 4)
        self.assertAlmostEqual(-0.1282, team_3_opponents_opponents_ranking, 4)
        self.assertAlmostEqual(0.1656, team_4_opponents_opponents_ranking, 4)

    def test_strength_of_schedules(self):
        team_1_strength_of_schedule = calculate_strength_of_schedule(
            self.team_1, self.results_chooser, self.rows_by_team
        )
        team_2_strength_of_schedule = calculate_strength_of_schedule(
            self.team_2, self.results_chooser, self.rows_by_team
        )
        team_3_strength_of_schedule = calculate_strength_of_schedule(
            self.team_3, self.results_chooser, self.rows_by_team
        )
        team_4_strength_of_schedule = calculate_strength_of_schedule(
            self.team_4, self.results_chooser, self.rows_by_team
        )

        self.assertAlmostEqual(0.2242, team_1_strength_of_schedule, 4)
        self.assertAlmostEqual(0.0506, team_2_strength_of_schedule, 4)
        self.assertAlmostEqual(-0.0616, team_3_strength_of_schedule, 4)
        self.assertAlmostEqual(0.0863, team_4_strength_of_schedule, 4)