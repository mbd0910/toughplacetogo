from django.test import TestCase

from football.league_table import GamePOV, LeagueTableRow
from football.models import Team


class LeagueTableRowTestCase(TestCase):
    def test_games_played(self):
        """Games played is wins + draws + losses"""
        charlton = Team(name='Charlton')
        league_table_row = LeagueTableRow(charlton)
        self.assertEqual(league_table_row.games_played(), 0)

        opposition1 = Team(name='Opposition 1')
        opposition2 = Team(name='Opposition 2')
        opposition3 = Team(name='Opposition 3')
        league_table_row.add_result(GamePOV(charlton, opposition1, scored=3, conceded=0, is_home=True))
        league_table_row.add_result(GamePOV(charlton, opposition2, scored=2, conceded=1, is_home=False))
        league_table_row.add_result(GamePOV(charlton, opposition3, scored=1, conceded=0, is_home=True))
        self.assertEqual(league_table_row.games_played(), 3)

    def test_points(self):
        """3 points for a win and 1 for a draw"""
        charlton = Team(name='Charlton')
        league_table_row = LeagueTableRow(Team(name='Charlton'))
        self.assertEqual(league_table_row.points(), 0)

        opposition1 = Team(name='Opposition 1')
        opposition2 = Team(name='Opposition 2')
        opposition3 = Team(name='Opposition 3')
        opposition4 = Team(name='Opposition 4')
        opposition5 = Team(name='Opposition 5')
        opposition6 = Team(name='Opposition 6')
        # 3 wins, 2 draws and 1 defeat = 3 * 3 + 2 = 11
        league_table_row.add_result(GamePOV(charlton, opposition1, scored=1, conceded=0, is_home=True))
        league_table_row.add_result(GamePOV(charlton, opposition2, scored=1, conceded=1, is_home=False))
        league_table_row.add_result(GamePOV(charlton, opposition3, scored=0, conceded=1, is_home=True))
        league_table_row.add_result(GamePOV(charlton, opposition4, scored=3, conceded=3, is_home=False))
        league_table_row.add_result(GamePOV(charlton, opposition5, scored=2, conceded=0, is_home=True))
        league_table_row.add_result(GamePOV(charlton, opposition6, scored=2, conceded=1, is_home=False))
        self.assertEqual(league_table_row.points(), 11)

    def test_most_recent_games(self):
        """Finds most recent games"""
        charlton = Team(name='Charlton')
        league_table_row = LeagueTableRow(Team(name='Charlton'))
        self.assertEqual(league_table_row.most_recent_games(), [])

        opposition1 = Team(name='Opposition 1')
        opposition2 = Team(name='Opposition 2')
        opposition3 = Team(name='Opposition 3')
        opposition4 = Team(name='Opposition 4')
        opposition5 = Team(name='Opposition 5')
        opposition6 = Team(name='Opposition 6')
        game_pov1 = GamePOV(charlton, opposition1, scored=1, conceded=0, is_home=False)
        game_pov2 = GamePOV(charlton, opposition2, scored=1, conceded=1, is_home=True)
        game_pov3 = GamePOV(charlton, opposition3, scored=0, conceded=1, is_home=False)
        game_pov4 = GamePOV(charlton, opposition4, scored=3, conceded=3, is_home=True)
        game_pov5 = GamePOV(charlton, opposition5, scored=2, conceded=0, is_home=False)
        game_pov6 = GamePOV(charlton, opposition6, scored=2, conceded=1, is_home=True)
        league_table_row.add_result(game_pov1)
        league_table_row.add_result(game_pov2)
        league_table_row.add_result(game_pov3)
        league_table_row.add_result(game_pov4)
        league_table_row.add_result(game_pov5)
        league_table_row.add_result(game_pov6)

        self.assertEqual(len(league_table_row.most_recent_games(1)), 1)
        self.assertEqual(len(league_table_row.most_recent_games(2)), 2)
        self.assertEqual(len(league_table_row.most_recent_games(3)), 3)
        self.assertEqual(len(league_table_row.most_recent_games(4)), 4)
        self.assertEqual(len(league_table_row.most_recent_games(5)), 5)
        self.assertEqual(len(league_table_row.most_recent_games(6)), 6)
        self.assertEqual(len(league_table_row.most_recent_games(7)), 6)

        most_recent_home_games = league_table_row.most_recent_games(3)
        self.assertNotIn(game_pov1, most_recent_home_games)
        self.assertNotIn(game_pov2, most_recent_home_games)
        self.assertNotIn(game_pov3, most_recent_home_games)
        self.assertIn(game_pov4, most_recent_home_games)
        self.assertIn(game_pov5, most_recent_home_games)
        self.assertIn(game_pov6, most_recent_home_games)

    def test_most_recent_home_games(self):
        """Finds most recent X home games"""
        charlton = Team(name='Charlton')
        league_table_row = LeagueTableRow(Team(name='Charlton'))
        self.assertEqual(league_table_row.most_recent_home_games(), [])

        opposition1 = Team(name='Opposition 1')
        opposition2 = Team(name='Opposition 2')
        opposition3 = Team(name='Opposition 3')
        opposition4 = Team(name='Opposition 4')
        opposition5 = Team(name='Opposition 5')
        opposition6 = Team(name='Opposition 6')
        game_pov1 = GamePOV(charlton, opposition1, scored=1, conceded=0, is_home=True)
        game_pov2 = GamePOV(charlton, opposition2, scored=1, conceded=1, is_home=True)
        game_pov3 = GamePOV(charlton, opposition3, scored=0, conceded=1, is_home=True)
        game_pov4 = GamePOV(charlton, opposition4, scored=3, conceded=3, is_home=False)
        game_pov5 = GamePOV(charlton, opposition5, scored=2, conceded=0, is_home=True)
        game_pov6 = GamePOV(charlton, opposition6, scored=2, conceded=1, is_home=True)
        league_table_row.add_result(game_pov1)
        league_table_row.add_result(game_pov2)
        league_table_row.add_result(game_pov3)
        league_table_row.add_result(game_pov4)
        league_table_row.add_result(game_pov5)
        league_table_row.add_result(game_pov6)

        self.assertEqual(len(league_table_row.most_recent_home_games(1)), 1)
        self.assertEqual(len(league_table_row.most_recent_home_games(2)), 2)
        self.assertEqual(len(league_table_row.most_recent_home_games(3)), 3)
        self.assertEqual(len(league_table_row.most_recent_home_games(4)), 4)
        self.assertEqual(len(league_table_row.most_recent_home_games(5)), 5)
        self.assertEqual(len(league_table_row.most_recent_home_games(6)), 5)

        most_recent_home_games = league_table_row.most_recent_home_games(3)
        self.assertNotIn(game_pov1, most_recent_home_games)
        self.assertNotIn(game_pov2, most_recent_home_games)
        self.assertNotIn(game_pov4, most_recent_home_games)
        self.assertIn(game_pov3, most_recent_home_games)
        self.assertIn(game_pov5, most_recent_home_games)
        self.assertIn(game_pov6, most_recent_home_games)

    def test_upcoming_games(self):
        """Test upcoming X games"""
        charlton = Team(name='Charlton')
        league_table_row = LeagueTableRow(Team(name='Charlton'))
        self.assertEqual(league_table_row.upcoming_games(), [])

        opposition1 = Team(name='Opposition 1')
        opposition2 = Team(name='Opposition 2')
        opposition3 = Team(name='Opposition 3')
        opposition4 = Team(name='Opposition 4')
        opposition5 = Team(name='Opposition 5')
        opposition6 = Team(name='Opposition 6')
        game_pov1 = GamePOV(charlton, opposition1, scored=1, conceded=0, is_home=True)
        game_pov2 = GamePOV(charlton, opposition2, scored=1, conceded=1, is_home=True)
        game_pov3 = GamePOV(charlton, opposition3, scored=0, conceded=1, is_home=True)
        game_pov4 = GamePOV(charlton, opposition4, scored=3, conceded=3, is_home=False)
        game_pov5 = GamePOV(charlton, opposition5, scored=2, conceded=0, is_home=True)
        game_pov6 = GamePOV(charlton, opposition6, scored=2, conceded=1, is_home=True)
        league_table_row.add_fixture(game_pov1)
        league_table_row.add_fixture(game_pov2)
        league_table_row.add_fixture(game_pov3)
        league_table_row.add_fixture(game_pov4)
        league_table_row.add_fixture(game_pov5)
        league_table_row.add_fixture(game_pov6)

        self.assertEqual(len(league_table_row.upcoming_games(1)), 1)
        self.assertEqual(len(league_table_row.upcoming_games(2)), 2)
        self.assertEqual(len(league_table_row.upcoming_games(3)), 3)
        self.assertEqual(len(league_table_row.upcoming_games(4)), 4)
        self.assertEqual(len(league_table_row.upcoming_games(5)), 5)
        self.assertEqual(len(league_table_row.upcoming_games(6)), 5)

        upcoming_games = league_table_row.upcoming_games(3)
        self.assertNotIn(game_pov4, upcoming_games)
        self.assertNotIn(game_pov5, upcoming_games)
        self.assertNotIn(game_pov6, upcoming_games)
        self.assertIn(game_pov1, upcoming_games)
        self.assertIn(game_pov2, upcoming_games)
        self.assertIn(game_pov3, upcoming_games)

    def test_most_recent_away_games(self):
        """Finds most recent X away games"""
        charlton = Team(name='Charlton')
        league_table_row = LeagueTableRow(charlton)
        self.assertEqual(league_table_row.most_recent_away_games(), [])

        opposition1 = Team(name='Opposition 1')
        opposition2 = Team(name='Opposition 2')
        opposition3 = Team(name='Opposition 3')
        opposition4 = Team(name='Opposition 4')
        opposition5 = Team(name='Opposition 5')
        opposition6 = Team(name='Opposition 6')
        game_pov1 = GamePOV(charlton, opposition1, scored=1, conceded=0, is_home=False)
        game_pov2 = GamePOV(charlton, opposition2, scored=1, conceded=1, is_home=True)
        game_pov3 = GamePOV(charlton, opposition3, scored=0, conceded=1, is_home=False)
        game_pov4 = GamePOV(charlton, opposition4, scored=3, conceded=3, is_home=False)
        game_pov5 = GamePOV(charlton, opposition5, scored=2, conceded=0, is_home=True)
        game_pov6 = GamePOV(charlton, opposition6, scored=2, conceded=1, is_home=False)
        league_table_row.add_result(game_pov1)
        league_table_row.add_result(game_pov2)
        league_table_row.add_result(game_pov3)
        league_table_row.add_result(game_pov4)
        league_table_row.add_result(game_pov5)
        league_table_row.add_result(game_pov6)

        self.assertEqual(len(league_table_row.most_recent_away_games(1)), 1)
        self.assertEqual(len(league_table_row.most_recent_away_games(2)), 2)
        self.assertEqual(len(league_table_row.most_recent_away_games(3)), 3)
        self.assertEqual(len(league_table_row.most_recent_away_games(4)), 4)
        self.assertEqual(len(league_table_row.most_recent_away_games(5)), 4)
        self.assertEqual(len(league_table_row.most_recent_away_games(6)), 4)

        most_recent_away_games = league_table_row.most_recent_away_games(2)
        self.assertNotIn(game_pov1, most_recent_away_games)
        self.assertNotIn(game_pov2, most_recent_away_games)
        self.assertNotIn(game_pov3, most_recent_away_games)
        self.assertNotIn(game_pov5, most_recent_away_games)
        self.assertIn(game_pov4, most_recent_away_games)
        self.assertIn(game_pov6, most_recent_away_games)

    def test_has_points_deducted_yes(self):
        league_table_row = LeagueTableRow(Team(name='Charlton'), points_deduction=2)
        self.assertTrue(league_table_row.has_points_deducted())

    def test_has_points_deducted_no(self):
        league_table_row = LeagueTableRow(Team(name='Charlton'), points_deduction=0)
        self.assertFalse(league_table_row.has_points_deducted())

    def test_points_with_points_deduction(self):
        league_table_row = LeagueTableRow(Team(name='Charlton'), points_deduction=16, wins=2, draws=1)
        self.assertEqual(-9, league_table_row.points())
        self.assertEqual(7, league_table_row.performance_points())

    def test_points_with_no_points_deduction(self):
        league_table_row = LeagueTableRow(Team(name='Charlton'), points_deduction=0, wins=4, draws=2)
        self.assertEqual(14, league_table_row.points())
        self.assertEqual(14, league_table_row.performance_points())

    def test_performance_points_per_game(self):
        charlton = Team(name='Charlton')
        league_table_row = LeagueTableRow(charlton)

        opposition1 = Team(name='Opposition 1')
        opposition2 = Team(name='Opposition 2')
        opposition3 = Team(name='Opposition 3')
        opposition4 = Team(name='Opposition 4')
        league_table_row.add_result(GamePOV(charlton, opposition1, scored=3, conceded=0, is_home=True))
        league_table_row.add_result(GamePOV(charlton, opposition2, scored=0, conceded=1, is_home=False))
        league_table_row.add_result(GamePOV(charlton, opposition3, scored=1, conceded=0, is_home=True))
        league_table_row.add_result(GamePOV(charlton, opposition4, scored=0, conceded=0, is_home=True))
        # 7 / 4 = 1.75
        self.assertEqual(1.75, league_table_row.performance_points_per_game())

    def test_x_points_per_game(self):
        charlton = Team(name='Charlton')
        league_table_row = LeagueTableRow(charlton)
        league_table_row.x_points = 9.3
        opposition1 = Team(name='Opposition 1')
        opposition2 = Team(name='Opposition 2')
        opposition3 = Team(name='Opposition 3')
        opposition4 = Team(name='Opposition 4')
        league_table_row.add_result(GamePOV(charlton, opposition1, scored=3, conceded=0, is_home=True))
        league_table_row.add_result(GamePOV(charlton, opposition2, scored=0, conceded=1, is_home=False))
        league_table_row.add_result(GamePOV(charlton, opposition3, scored=1, conceded=0, is_home=True))
        league_table_row.add_result(GamePOV(charlton, opposition4, scored=0, conceded=0, is_home=True))
        league_table_row.add_result(GamePOV(charlton, opposition1, scored=0, conceded=0, is_home=False))
        # 9.3 / 5 = 1.86
        self.assertEqual(1.86, league_table_row.x_points_per_game())

    def test_xg_difference(self):
        charlton = Team(name='Charlton')
        league_table_row = LeagueTableRow(charlton)
        league_table_row.xg = 2.4
        league_table_row.xg_against = 3.1

        self.assertAlmostEqual(-0.7, league_table_row.xg_difference())

    def test_xg_difference_per_game(self):
        charlton = Team(name='Charlton')
        league_table_row = LeagueTableRow(charlton)
        opposition1 = Team(name='Opposition 1')
        opposition2 = Team(name='Opposition 2')
        league_table_row.add_result(GamePOV(charlton, opposition1, scored=3, conceded=0, is_home=True))
        league_table_row.add_result(GamePOV(charlton, opposition2, scored=0, conceded=1, is_home=False))
        league_table_row.xg = 3.1
        league_table_row.xg_against = 2.3
        self.assertAlmostEqual(0.4, league_table_row.xg_difference_per_game())

    def test_goal_difference(self):
        charlton = Team(name='Charlton')
        league_table_row = LeagueTableRow(charlton)
        opposition1 = Team(name='Opposition 1')
        opposition2 = Team(name='Opposition 2')
        league_table_row.add_result(GamePOV(charlton, opposition1, scored=2, conceded=3, is_home=True))
        league_table_row.add_result(GamePOV(charlton, opposition2, scored=0, conceded=1, is_home=False))
        # 2 - 4
        self.assertEqual(-2, league_table_row.goal_difference())

    def test_goal_difference_per_game(self):
        charlton = Team(name='Charlton')
        league_table_row = LeagueTableRow(charlton)
        opposition1 = Team(name='Opposition 1')
        opposition2 = Team(name='Opposition 2')
        league_table_row.add_result(GamePOV(charlton, opposition1, scored=2, conceded=1, is_home=True))
        league_table_row.add_result(GamePOV(charlton, opposition2, scored=2, conceded=1, is_home=False))
        league_table_row.add_result(GamePOV(charlton, opposition2, scored=5, conceded=4, is_home=False))
        # (9 - 6) / 3
        self.assertEqual(1, league_table_row.goal_difference_per_game())