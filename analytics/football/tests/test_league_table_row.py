from django.test import TestCase

from football.league_table import LeagueTableRow


class LeagueTableRowTestCase(TestCase):
    def test_games_played(self):
        """Games played is wins + draws + losses"""
        empty_league_table_row = LeagueTableRow('Charlton')
        self.assertEqual(empty_league_table_row.games_played(), 0)

        several_games_league_table_row = LeagueTableRow('Charlton', 5, 4, 3)
        self.assertEqual(several_games_league_table_row.games_played(), 12)
