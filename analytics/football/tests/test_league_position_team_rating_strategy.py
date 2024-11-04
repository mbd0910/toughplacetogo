from django.test import TestCase

from football.league_table import GamePOV, LeagueTableRow
from football.modelling.team_rating_strategy import LeaguePositionTeamRatingStrategy
from football.models import Team


class LeaguePositionTeamRatingStrategyTestCase(TestCase):
    def test_team_ratings_no_goal_difference(self):
        galatasaray = Team(id=1, name='Galatasaray')
        man_utd = Team(id=2, name='Manchester United')
        copenhagen = Team(id=3, name='Copenhagen')
        bayern = Team(id=4, name='Bayern Munich')

        galatasaray_row = LeagueTableRow(team=galatasaray, wins=1, draws=2)
        man_utd_row = LeagueTableRow(team=man_utd, wins=1, draws=1)
        copenhagen_row = LeagueTableRow(team=copenhagen, wins=2, draws=2)
        bayern_row = LeagueTableRow(team=bayern, wins=5, draws=1)

        rows_by_team = {
            galatasaray: galatasaray_row,
            man_utd: man_utd_row,
            copenhagen: copenhagen_row,
            bayern: bayern_row
        }

        league_position_team_rating_strategy = LeaguePositionTeamRatingStrategy()
        team_ratings = league_position_team_rating_strategy.calculate_team_ratings(rows_by_team)

        self.assertEqual(4, team_ratings[bayern])
        self.assertEqual(3, team_ratings[copenhagen])
        self.assertEqual(2, team_ratings[galatasaray])
        self.assertEqual(1, team_ratings[man_utd])

    def test_team_ratings_goal_difference_and_goals_scored(self):
        real_sociedad = Team(id=1, name='Real Sociedad')
        inter = Team(id=2, name='Internazionale')
        benfica = Team(id=3, name='Benfica')
        rb_salzburg = Team(id=4, name='Red Bull Salzburg')

        real_sociedad_row = LeagueTableRow(team=real_sociedad)
        inter_row = LeagueTableRow(team=inter)
        benfica_row = LeagueTableRow(team=benfica)
        rb_salzburg_row = LeagueTableRow(team=rb_salzburg)

        def add_result(home_team_row: LeagueTableRow, away_team_row: LeagueTableRow,
                       home_goals: int, away_goals: int):
            home_team_row.add_result(GamePOV(home_team_row.team, away_team_row.team, is_home=True, scored=home_goals, conceded=away_goals))
            away_team_row.add_result(GamePOV(away_team_row.team, home_team_row.team, is_home=False, scored=away_goals, conceded=home_goals))

        add_result(benfica_row, rb_salzburg_row, 0, 2)
        add_result(real_sociedad_row, inter_row, 1, 1)
        add_result(rb_salzburg_row, real_sociedad_row, 0, 2)
        add_result(inter_row, benfica_row, 1, 0)
        add_result(inter_row, rb_salzburg_row, 2, 1)
        add_result(benfica_row, real_sociedad_row, 0, 1)
        add_result(real_sociedad_row, benfica_row, 3, 1)
        add_result(rb_salzburg_row, inter_row, 0, 1)
        add_result(benfica_row, inter_row, 3, 3)
        add_result(real_sociedad_row, rb_salzburg_row, 0, 0)
        add_result(rb_salzburg_row, benfica_row, 1, 3)
        add_result(inter_row, real_sociedad_row, 0, 0)

        rows_by_team = {
            real_sociedad: real_sociedad_row,
            inter: inter_row,
            benfica: benfica_row,
            rb_salzburg: rb_salzburg_row
        }

        league_position_team_rating_strategy = LeaguePositionTeamRatingStrategy()
        team_ratings = league_position_team_rating_strategy.calculate_team_ratings(rows_by_team)

        self.assertEqual(4, team_ratings[real_sociedad])
        self.assertEqual(3, team_ratings[inter])
        self.assertEqual(2, team_ratings[benfica])
        self.assertEqual(1, team_ratings[rb_salzburg])

