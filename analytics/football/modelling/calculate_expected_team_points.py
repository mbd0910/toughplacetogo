from football.modelling.scoreline_probability_distribution import ScorelineProbabilityDistribution


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
