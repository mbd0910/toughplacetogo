import math
import numpy as np
from scipy.optimize import minimize
from scipy.stats import poisson
from match_odds import MatchOdds
from odds import Odds
from total_goals_odds import TotalGoalsOdds
from asian_handicap_odds import AsianHandicapOdds
from functools import partial


def quarter_line_half_loss(exceed_probability, push_probability):
    return exceed_probability / (1 - (push_probability/2))


def quarter_line_half_win(exceed_probability, push_probability):
    return (exceed_probability - (push_probability/2)) / (1 - (push_probability/2))


def half_or_whole_line(exceed_probability, push_probability):
    return exceed_probability / (1 - push_probability)


def tg_line_details(line):
    # Split the float into its fractional and integral parts
    fractional, integral = math.modf(line)

    # Check if the fractional part is .25 or .75
    if fractional == 0.0:
        return {'exceed': line, 'push': line, 'function': half_or_whole_line}
    elif fractional == 0.25:
        return {'push': integral, 'exceed': integral + 0.5, 'function': quarter_line_half_loss}
    elif fractional == 0.5:
        return {'exceed': line, 'push': line, 'function': half_or_whole_line}
    elif fractional == 0.75:
        return {'exceed': integral + 0.5, 'push': integral + 1.0, 'function': quarter_line_half_win}
    else:
        raise Exception(f"Unsupported fractional suffix in {line}")


def hcp_line_details(line):
    fractional, integral = math.modf(line)
    fractional = abs(fractional)
    # fractional_part = abs(line) - int(abs(line))  # Get the fractional part of the line (absolute value)

    if fractional == 0.0:
        return {'exceed': line, 'push': line, 'function': half_or_whole_line}
    elif fractional == 0.25:
        function = quarter_line_half_loss if line < 0 else quarter_line_half_win
        exceed_offset = -0.5 if line < 0 else 0.5
        return {'exceed': integral + exceed_offset, 'push': integral, 'function': function}
    elif fractional == 0.5:
        return {'exceed': line, 'push': line, 'function': half_or_whole_line}
    elif fractional == 0.75:
        function = quarter_line_half_win if line < 0 else quarter_line_half_loss
        exceed_offset = -0.5 if line < 0 else 0.5
        push_offset = -1 if line < 0 else 1
        return {'exceed': integral + exceed_offset, 'push': integral + push_offset, 'function': function}
    else:
        raise Exception(f"Unsupported fractional suffix in {line}")

# Test the function with some examples
# test_lines = [-1.75, -1.5, -1.25, -1, -0.75, -0.5, -0.25, 0, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 1.75]
# results = {line: asian_handicap_result(line) for line in test_lines}
# print(results)
# exit(0)


def error(par,
          home_fair_probability,
          draw_fair_probability,
          away_fair_probability,
          over_fair_probability,
          under_fair_probability,
          tg_push_line,
          tg_exceed_line,
          tg_function,
          handicap_home_fair_probability,
          handicap_away_fair_probability,
          hcp_push_line,
          hcp_exceed_line,
          hcp_function):
    home_xg = np.exp(par[0])
    away_xg = np.exp(par[1])

    home_sum = away_sum = draw_sum = 0
    tg_exceed_sum = tg_push_sum = 0
    hcp_exceed_sum = hcp_push_sum = 0

    for i in range(16):
        for j in range(16):
            prob = poisson.pmf(i, home_xg) * poisson.pmf(j, away_xg)
            if i > j:
                home_sum += prob
            elif i < j:
                away_sum += prob
            else:
                draw_sum += prob

            if i + j > tg_exceed_line:
                tg_exceed_sum += prob

            if i + j == tg_push_line:
                tg_push_sum += prob

            if i + j + hcp_exceed_line > 0:
                hcp_exceed_sum += prob

            if i + j + hcp_push_line == 0:
                hcp_push_sum += prob

    overs_sum = tg_function(tg_exceed_sum, tg_push_sum)
    unders_sum = 1 - overs_sum

    hcp_home_sum = hcp_function(hcp_exceed_sum, hcp_push_sum)
    hcp_away_sum = 1 - hcp_home_sum

    # print(f"Exceed line is {tg_exceed_line}")
    # print(f"Push line is {tg_push_line}")
    # print(f"Overs fair probability {overs_sum}")
    # print(f"Unders fair probability {unders_sum}")
    # print(f"HCP home fair probability {hcp_home_sum}")
    # print(f"HCP away fair probability {hcp_away_sum}")
    # print(home_sum)
    # print(away_sum)
    # print(draw_sum)

    return (
            (home_sum - home_fair_probability)**2 +
            (away_sum - away_fair_probability)**2 +
            (draw_sum - draw_fair_probability)**2 +
            (overs_sum - over_fair_probability)**2 +
            (unders_sum - under_fair_probability)**2 +
            (hcp_home_sum - handicap_home_fair_probability)**2 +
            (hcp_away_sum - handicap_away_fair_probability)**2)


def find_expected_goals(
        match_odds: MatchOdds,
        asian_handicap_odds: AsianHandicapOdds,
        total_goals_odds: TotalGoalsOdds):
    home_fair_probability = match_odds.home_fair_probability()
    draw_fair_probability = match_odds.draw_fair_probability()
    away_fair_probability = match_odds.away_probability()
    over_fair_probability = total_goals_odds.over_fair_probability()
    under_fair_probability = total_goals_odds.under_fair_probability()
    handicap_home_fair_probability = asian_handicap_odds.home_fair_probability()
    handicap_away_fair_probability = asian_handicap_odds.away_fair_probability()

    tg_line_metadata = tg_line_details(total_goals_odds.line)
    tg_push_line = tg_line_metadata['push']
    tg_exceed_line = tg_line_metadata['exceed']
    tg_function = tg_line_metadata['function']

    hcp_line_metadata = hcp_line_details(asian_handicap_odds.home_line)
    hcp_push_line = hcp_line_metadata['push']
    hcp_exceed_line = hcp_line_metadata['exceed']
    hcp_function = hcp_line_metadata['function']

    error_with_params = partial(
        error,
        home_fair_probability=home_fair_probability,
        draw_fair_probability=draw_fair_probability,
        away_fair_probability=away_fair_probability,
        over_fair_probability=over_fair_probability,
        under_fair_probability=under_fair_probability,
        tg_push_line=tg_push_line,
        tg_exceed_line=tg_exceed_line,
        tg_function=tg_function,
        handicap_home_fair_probability=handicap_home_fair_probability,
        handicap_away_fair_probability=handicap_away_fair_probability,
        hcp_push_line=hcp_push_line,
        hcp_exceed_line=hcp_exceed_line,
        hcp_function=hcp_function
    )

    initial_home_goals_estimate = (total_goals_odds.line - asian_handicap_odds.home_line) / 2
    initial_away_goals_estimate = total_goals_odds.line - initial_home_goals_estimate
    initial_guess = np.log([initial_home_goals_estimate, initial_away_goals_estimate])

    # Use minimize function from scipy.optimize to find the optimal parameters
    result = minimize(
        fun=error_with_params,
        x0=initial_guess,
        method='Nelder-Mead'
    )
    goals = np.exp(result.x)

    print(f"Home: {goals[0]}, Away: {goals[1]}")
    print(f"TG: {goals[0] + goals[1]}")
    print(f"HCP: {goals[0] - goals[1]}")


match_odds = MatchOdds(
    home=Odds(1.15),
    draw=Odds(10),
    away=Odds(25)
)

total_goals_odds = TotalGoalsOdds(
    line=3.25,
    under=Odds(2.01),
    over=Odds(1.85)
)

asian_handicap_odds = AsianHandicapOdds(
    home_line=-2.25,
    home_odds=Odds(1.98),
    away_line=2.25,
    away_odds=Odds(1.94)
)

find_expected_goals(match_odds, asian_handicap_odds, total_goals_odds)
