from football.modelling.expected_goals import ExpectedGoals
from football.modelling.scoreline_probability_distribution import ScorelineProbabilityDistribution
from football.trading.asian_handicap_odds import AsianHandicapOdds
from football.trading.betfair_event import BetfairEvent
from football.trading.match_odds import MatchOdds
from football.trading.total_goals_odds import TotalGoalsOdds


class EFLGamePrediction:
    def __init__(self,
                 betfair_event: BetfairEvent,
                 match_odds: MatchOdds,
                 asian_handicap_odds: AsianHandicapOdds,
                 total_goals_odds: TotalGoalsOdds,
                 expected_goals: ExpectedGoals,
                 scoreline_probability_distribution: ScorelineProbabilityDistribution,
                 expected_home_points: float,
                 expected_away_points):
        self.betfair_event = betfair_event
        self.match_odds = match_odds
        self.asian_handicap_odds = asian_handicap_odds
        self.total_goals_odds = total_goals_odds
        self.expected_goals = expected_goals
        self.scoreline_probability_distribution = scoreline_probability_distribution
        self.expected_home_points = expected_home_points
        self.expected_away_points = expected_away_points

    def clean_sheet_probability_by_team(self, team_name):
        if self.is_home_team(team_name):
            return self.scoreline_probability_distribution.home_clean_sheet_probability()
        else:
            return self.scoreline_probability_distribution.away_clean_sheet_probability()

    def score_more_than_two_probability_by_team(self, team_name):
        if self.is_home_team(team_name):
            return self.scoreline_probability_distribution.home_two_or_more_goals_probability()
        else:
            return self.scoreline_probability_distribution.away_two_or_more_goals_probability()

    def win_probability_by_team(self, team_name):
        if self.is_home_team(team_name):
            return self.scoreline_probability_distribution.home_win_probability()
        else:
            return self.scoreline_probability_distribution.away_win_probability()

    def match_odds_win_probability_by_team(self, team_name):
        return self.match_odds.home.implied_probability() \
            if self.is_home_team(team_name) else self.match_odds.away.implied_probability()

    def is_home_team(self, team_name):
        return team_name == self.betfair_event.home_team

    def opposition(self, team_name):
        return self.betfair_event.away_team if self.is_home_team(team_name) else self.betfair_event.home_team

    def team_handicap_line(self, team_name):
        return self.asian_handicap_odds.home_line \
            if self.is_home_team(team_name) else self.asian_handicap_odds.away_line

    def total_overround(self):
        return self.match_odds.overround() + self.total_goals_odds.overround() + self.asian_handicap_odds.overround()

    def total_matched(self):
        return self.match_odds.total_matched + self.total_goals_odds.total_matched + self.asian_handicap_odds.total_matched