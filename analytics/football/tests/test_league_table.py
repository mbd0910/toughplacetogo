from django.test import TestCase

from football.league_table import LeagueTable, LeagueTableRow
from football.models import Team


class LeagueTableTestCase(TestCase):
    def test_team_to_position(self):
        """Team to position in the league"""
        team1 = Team(id=1, name='Team 1')
        team2 = Team(id=2, name='Team 2')
        team3 = Team(id=3, name='Team 3')
        league_table = LeagueTable(
            [
                LeagueTableRow(team=team2),
                LeagueTableRow(team=team3),
                LeagueTableRow(team=team1)
            ]
        )

        team_to_position = league_table.team_to_position()

        self.assertEqual(len(team_to_position), 3)
        self.assertEqual(team_to_position[team1], 3)
        self.assertEqual(team_to_position[team2], 1)
        self.assertEqual(team_to_position[team3], 2)