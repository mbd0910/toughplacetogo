from expected_goals import ExpectedGoals
from scoreline_probability_distribution import ScorelineProbabilityDistribution
from match_odds import MatchOdds
from asian_handicap_odds import AsianHandicapOdds
from total_goals_odds import TotalGoalsOdds


class EFLGamePrediction:
    def __init__(self,
                 event_name: str,
                 match_odds: MatchOdds,
                 asian_handicap_odds: AsianHandicapOdds,
                 total_goals_odds: TotalGoalsOdds,
                 expected_goals: ExpectedGoals,
                 scoreline_probability_distribution: ScorelineProbabilityDistribution,
                 expected_home_points: float,
                 expected_away_points):
        self.event_name = event_name
        self.match_odds = match_odds
        self.asian_handicap_odds = asian_handicap_odds
        self.total_goals_odds = total_goals_odds
        self.expected_goals = expected_goals
        self.scoreline_probability_distribution = scoreline_probability_distribution
        self.expected_home_points = expected_home_points
        self.expected_away_points = expected_away_points
