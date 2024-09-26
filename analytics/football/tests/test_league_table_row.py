from django.test import TestCase

from football.league_table import GamePOV, LeagueTableRow
from football.models import Team


class LeagueTableRowTestCase(TestCase):
    def test_games_played(self):
        """Games played is wins + draws + losses"""
        charlton = Team(name='Charlton')
        league_table_row = LeagueTableRow(Team(name='Charlton'))
        self.assertEqual(league_table_row.games_played(), 0)

        opposition1 = Team(name='Opposition 1')
        opposition2 = Team(name='Opposition 2')
        opposition3 = Team(name='Opposition 3')
        league_table_row.add_game_pov(GamePOV(charlton, opposition1, 3, 0, is_home=True))
        league_table_row.add_game_pov(GamePOV(charlton, opposition2, 2, 1, is_home=False))
        league_table_row.add_game_pov(GamePOV(charlton, opposition3, 1, 0, is_home=True))
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
        league_table_row.add_game_pov(GamePOV(charlton, opposition1, 1, 0, is_home=True))
        league_table_row.add_game_pov(GamePOV(charlton, opposition2, 1, 1, is_home=False))
        league_table_row.add_game_pov(GamePOV(charlton, opposition3, 0, 1, is_home=True))
        league_table_row.add_game_pov(GamePOV(charlton, opposition4, 3, 3, is_home=False))
        league_table_row.add_game_pov(GamePOV(charlton, opposition5, 2, 0, is_home=True))
        league_table_row.add_game_pov(GamePOV(charlton, opposition6, 2, 1, is_home=False))
        self.assertEqual(league_table_row.points(), 11)
