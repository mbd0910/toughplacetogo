from odds import Odds
from match_odds import MatchOdds
from asian_handicap_odds import AsianHandicapOdds
from total_goals_odds import TotalGoalsOdds
import math
from scoreline_probability_distribution import ScorelineProbabilityDistribution


HOME_WIN_POINTS = 5
DRAW_POINTS = 3
AWAY_WIN_POINTS = 7
CLEAN_SHEET_POINTS = 2
TWO_OR_MORE_GOALS_POINTS = 2


def calculate_expected_home_team_points(scoreline_probability_distribution: ScorelineProbabilityDistribution):
    return (scoreline_probability_distribution.home_win_probability() * HOME_WIN_POINTS +
            scoreline_probability_distribution.draw_probability() * DRAW_POINTS +
            scoreline_probability_distribution.home_clean_sheet_probability() * CLEAN_SHEET_POINTS +
            scoreline_probability_distribution.home_two_or_more_goals_probability())


def calculate_expected_away_team_points(scoreline_probability_distribution: ScorelineProbabilityDistribution):
    return (scoreline_probability_distribution.away_win_probability() * AWAY_WIN_POINTS +
            scoreline_probability_distribution.draw_probability() * DRAW_POINTS +
            scoreline_probability_distribution.away_clean_sheet_probability() * CLEAN_SHEET_POINTS +
            scoreline_probability_distribution.away_two_or_more_goals_probability())


def calculate_expected_team_points(match_odds: MatchOdds):
    return match_odds.home.implied_probability() * 5


def calculate_expected_goals(asian_handicap_odds: AsianHandicapOdds, total_goals_odds: TotalGoalsOdds):
    implied_home_handicap_probability = asian_handicap_odds.home_odds.implied_probability()
    implied_away_handicap_probability = asian_handicap_odds.away_odds.implied_probability()

    print(implied_home_handicap_probability)
    print(implied_away_handicap_probability)

    implied_unders_probability = total_goals_odds.under.implied_probability()
    implied_overs_probability = total_goals_odds.over.implied_probability()

    print(implied_unders_probability)
    print(implied_overs_probability)

    implied_home_handicap_probability, implied_away_handicap_probability = (
        normalise_probabilities(implied_home_handicap_probability, implied_away_handicap_probability)
    )
    implied_unders_probability, implied_overs_probability = (
        normalise_probabilities(implied_unders_probability, implied_overs_probability)
    )

    print(implied_home_handicap_probability)
    print(implied_away_handicap_probability)
    print(implied_unders_probability)
    print(implied_overs_probability)

    # This definitely needs checking to make sure we bring the lines closer together/further apart as necessary
    # handicap_probability_difference = implied_home_handicap_probability - implied_away_handicap_probability
    # fair_home_line = asian_handicap_odds.home_line - handicap_probability_difference / 2
    #
    # print(handicap_probability_difference)
    # print(fair_home_line)

    expected_total_goals = (implied_overs_probability * math.ceil(total_goals_odds.line) +
                            implied_unders_probability * math.floor(total_goals_odds.line))

    print(expected_total_goals)

    # expected_home_goals = (expected_total_goals + fair_home_line) / 2
    # expected_away_goals = (expected_total_goals - fair_home_line) / 2
    #
    # return expected_home_goals, expected_away_goals


# To remove overround
def normalise_probabilities(one, two):
    total = one + two
    return one / total, two / total



if __name__ == "__main__":
    calculate_expected_goals(
        AsianHandicapOdds(0.5, Odds(1.94), -0.5, Odds(2.02)),
        TotalGoalsOdds(2.5, Odds(3.1), Odds(1.45))
    )
