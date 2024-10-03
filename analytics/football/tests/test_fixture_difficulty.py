from django.test import TestCase

from football.league_table import LeagueTableRow, GamePOV, calculate_fixture_difficulty
from football.models import Team


class LeagueTableTestCase(TestCase):
    def test_calculate_fixture_difficulty(self):
        """Calculates average fixture difficulty"""
        team1 = Team(id=1, name='Team 1')
        team2 = Team(id=2, name='Team 2')
        team3 = Team(id=3, name='Team 3')
        team4 = Team(id=4, name='Team 4')
        team5 = Team(id=5, name='Team 5')
        team6 = Team(id=6, name='Team 6')
        team7 = Team(id=7, name='Team 7')
        team8 = Team(id=8, name='Team 8')
        team9 = Team(id=9, name='Team 9')
        team_to_position = {
            team1: 1,
            team2: 2,
            team3: 3,
            team4: 4,
            team5: 5,
            team6: 6,
            team7: 7,
            team8: 8,
            team9: 9,
        }
        game_pov1 = GamePOV(team=team1, opposition=team3, scored=1, conceded=0, is_home=True)
        game_pov2 = GamePOV(team=team1, opposition=team5, scored=1, conceded=0, is_home=False)
        game_pov3 = GamePOV(team=team1, opposition=team7, scored=1, conceded=0, is_home=False)
        game_pov4 = GamePOV(team=team1, opposition=team8, scored=1, conceded=0, is_home=True)
        game_povs = [game_pov1, game_pov2, game_pov3, game_pov4]
        league_table_row = LeagueTableRow(team=team1, game_povs=game_povs)

        fixture_difficulty = calculate_fixture_difficulty(league_table_row, team_to_position)

        self.assertEqual(5.75, fixture_difficulty.average_position)