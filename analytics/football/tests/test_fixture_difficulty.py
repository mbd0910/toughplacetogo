from django.test import TestCase

from football.league_table import LeagueTableRow, GamePOV, LeagueTable, calculate_fixture_difficulties, \
    calculate_fixture_difficulty, weight_fixture_difficulties
from football.models import Team


class FixtureDifficultyTestCase(TestCase):
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

        league_table_position_fixture_difficulty = calculate_fixture_difficulty(league_table_row, team_to_position)

        self.assertEqual(4.75, league_table_position_fixture_difficulty)

    def test_calculate_fixture_difficulties(self):
        """Calculates fixture difficulties for all teams in league"""
        team1 = Team(id=1, name='Team 1')
        team2 = Team(id=2, name='Team 2')
        team3 = Team(id=3, name='Team 3')
        team4 = Team(id=4, name='Team 4')
        team5 = Team(id=5, name='Team 5')
        team6 = Team(id=6, name='Team 6')
        # A bit convoluted - ignore the scored and conceded values
        team1_game_povs = [
            GamePOV(team=team1, opposition=team2, scored=0, conceded=0, is_home=True),
            GamePOV(team=team1, opposition=team4, scored=0, conceded=0, is_home=True),
            GamePOV(team=team1, opposition=team6, scored=0, conceded=0, is_home=True),
        ]
        team2_game_povs = [
            GamePOV(team=team2, opposition=team1, scored=0, conceded=0, is_home=False),
            GamePOV(team=team2, opposition=team3, scored=0, conceded=0, is_home=True)
        ]
        team3_game_povs = [
            GamePOV(team=team3, opposition=team2, scored=0, conceded=0, is_home=False),
            GamePOV(team=team3, opposition=team6, scored=0, conceded=0, is_home=True)
        ]
        team4_game_povs = [
            GamePOV(team=team4, opposition=team1, scored=0, conceded=0, is_home=False),
            GamePOV(team=team4, opposition=team5, scored=0, conceded=0, is_home=False)
        ]
        team5_game_povs = [
            GamePOV(team=team5, opposition=team4, scored=0, conceded=0, is_home=True)
        ]
        team6_game_povs = [
            GamePOV(team=team6, opposition=team1, scored=0, conceded=0, is_home=False),
            GamePOV(team=team6, opposition=team3, scored=0, conceded=0, is_home=False)
        ]

        team1_row = LeagueTableRow(team=team1, game_povs=team1_game_povs)
        team2_row = LeagueTableRow(team=team2, game_povs=team2_game_povs)
        team3_row = LeagueTableRow(team=team3, game_povs=team3_game_povs)
        team4_row = LeagueTableRow(team=team4, game_povs=team4_game_povs)
        team5_row = LeagueTableRow(team=team5, game_povs=team5_game_povs)
        team6_row = LeagueTableRow(team=team6, game_povs=team6_game_povs)

        league_table = LeagueTable(
            [
                team1_row,
                team2_row,
                team3_row,
                team4_row,
                team5_row,
                team6_row
            ]
        )

        fixture_difficulties = calculate_fixture_difficulties(league_table)

        self.assertEqual(6, len(fixture_difficulties))
        self.assertEqual(3, fixture_difficulties[team1])
        self.assertEqual(1.5, fixture_difficulties[team2])
        self.assertEqual(3.5, fixture_difficulties[team3])
        self.assertEqual(2.5, fixture_difficulties[team4])
        self.assertEqual(4, fixture_difficulties[team5])
        self.assertEqual(2, fixture_difficulties[team6])

    def test_weight_fixture_difficulties(self):
        """Calculates weighted fixture difficulties for all teams in league"""
        charlton = Team(id=1, name='Charlton')
        another_team = Team(id=2, name='Another team')
        last_team = Team(id=3, name='Last team')
        league_position_fixture_difficulties = {
            charlton: 0.5,
            another_team: -0.4,
            last_team: -0.2
        }
        x_points_fixture_difficulties = {
            charlton: 0.8,
            another_team: 0.1,
            last_team: -0.45
        }
        weighted_fixture_difficulties = weight_fixture_difficulties(
            0.7, league_position_fixture_difficulties,
            0.3, x_points_fixture_difficulties
        )

        self.assertEqual(3, len(weighted_fixture_difficulties))
        self.assertAlmostEqual(0.59, weighted_fixture_difficulties.get(charlton))
        self.assertAlmostEqual(-0.25, weighted_fixture_difficulties.get(another_team))
        self.assertAlmostEqual(-0.275, weighted_fixture_difficulties.get(last_team))
        