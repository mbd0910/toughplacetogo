import math
import numpy as np
from scipy.optimize import minimize
from scipy.stats import poisson

# Define initial odds
HOME_BOOKIE_ODDS = 1.15
AWAY_BOOKIE_ODDS = 25
DRAW_BOOKIE_ODDS = 10

# Convert odds to probabilities
total_sum = 1/HOME_BOOKIE_ODDS + 1/AWAY_BOOKIE_ODDS + 1/DRAW_BOOKIE_ODDS
HOME_FAIR_PROBABILITY = 1/HOME_BOOKIE_ODDS/total_sum
AWAY_FAIR_PROBABILITY = 1/AWAY_BOOKIE_ODDS/total_sum
DRAW_FAIR_PROBABILITY = 1/DRAW_BOOKIE_ODDS/total_sum

tg_line = 3.25
OVER_BOOKIE_ODDS = 1.85
UNDER_BOOKIE_ODDS = 2.01
total_sum = 1/OVER_BOOKIE_ODDS + 1/UNDER_BOOKIE_ODDS
print(f"total sum is {total_sum}")
OVER_FAIR_PROBABILITY = 1/OVER_BOOKIE_ODDS/total_sum
UNDER_FAIR_PROBABILITY = 1/UNDER_BOOKIE_ODDS/total_sum
OVER_FAIR_ODDS = 1/OVER_FAIR_PROBABILITY
UNDER_FAIR_ODDS = 1/UNDER_FAIR_PROBABILITY

print(f"Bookie odds were overs: {OVER_BOOKIE_ODDS}")
print(f"Bookie odds were unders: {UNDER_BOOKIE_ODDS}")
print(f"Over is {OVER_FAIR_ODDS}")
print(f"Under is {UNDER_FAIR_ODDS}")

hcp_line = -2.25
HCP_HOME_BOOKIE_ODDS = 1.98
HCP_AWAY_BOOKIE_ODDS = 1.94
total_hcp_sum = 1/HOME_BOOKIE_ODDS + 1/AWAY_BOOKIE_ODDS
HCP_HOME_FAIR_PROBABILITY = 1/HCP_HOME_BOOKIE_ODDS/total_hcp_sum
HCP_AWAY_FAIR_PROBABILITY = 1/HCP_AWAY_BOOKIE_ODDS/total_hcp_sum
HCP_HOME_FAIR_ODDS = 1/HCP_HOME_FAIR_PROBABILITY
HCP_AWAY_FAIR_ODDS = 1/HCP_AWAY_FAIR_PROBABILITY


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


def error(par):
    home_xg = np.exp(par[0])
    away_xg = np.exp(par[1])

    home_sum = away_sum = draw_sum = 0
    tg_line_metadata = tg_line_details(tg_line)
    tg_push_line = tg_line_metadata['push']
    tg_exceed_line = tg_line_metadata['exceed']
    tg_function = tg_line_metadata['function']
    tg_exceed_sum = tg_push_sum = 0

    hcp_line_metadata = hcp_line_details(hcp_line)
    hcp_push_line = hcp_line_metadata['push']
    hcp_exceed_line = hcp_line_metadata['exceed']
    hcp_function = hcp_line_metadata['function']
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

    print(f"Exceed line is {tg_exceed_line}")
    print(f"Push line is {tg_push_line}")
    print(f"Overs fair probability {overs_sum}")
    print(f"Unders fair probability {unders_sum}")
    print(f"HCP home fair probability {hcp_home_sum}")
    print(f"HCP away fair probability {hcp_away_sum}")
    print(home_sum)
    print(away_sum)
    print(draw_sum)

    return (
            (home_sum - HOME_FAIR_PROBABILITY)**2 +
            (away_sum - AWAY_FAIR_PROBABILITY)**2 +
            (draw_sum - DRAW_FAIR_PROBABILITY)**2 +
            (overs_sum - OVER_FAIR_PROBABILITY)**2 +
            (unders_sum - UNDER_FAIR_PROBABILITY)**2 +
            (hcp_home_sum - HCP_HOME_FAIR_PROBABILITY)**2 +
            (hcp_away_sum - HCP_AWAY_FAIR_PROBABILITY)**2)


# Use minimize function from scipy.optimize to find the optimal parameters
result = minimize(error, [0, 0], method='Nelder-Mead')
goals = np.exp(result.x)

print(f"Home: {goals[0]}, Away: {goals[1]}")
print(f"TG: {goals[0] + goals[1]}")
print(f"HCP: {goals[0] - goals[1]}")
