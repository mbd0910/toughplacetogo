import math
import numpy as np
from scipy.optimize import minimize
from scipy.stats import poisson

# Define initial odds
HOME_BOOKIE_ODDS = 1.87
AWAY_BOOKIE_ODDS = 4.3
DRAW_BOOKIE_ODDS = 4.1

# Convert odds to probabilities
total_sum = 1/HOME_BOOKIE_ODDS + 1/AWAY_BOOKIE_ODDS + 1/DRAW_BOOKIE_ODDS
HOME_FAIR_PROBABILITY = 1/HOME_BOOKIE_ODDS/total_sum
AWAY_FAIR_PROBABILITY = 1/AWAY_BOOKIE_ODDS/total_sum
DRAW_FAIR_PROBABILITY = 1/DRAW_BOOKIE_ODDS/total_sum

tg_line = 2.75
OVER_BOOKIE_ODDS = 2.04
UNDER_BOOKIE_ODDS = 1.9
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


def find_nearest_tg_lines(value):
    # Split the float into its fractional and integral parts
    fractional, integral = math.modf(value)

    # Check if the fractional part is .25 or .75
    if fractional == 0.0:
        return {'exceed': integral, 'push': integral, 'function': half_or_whole_line}
    elif fractional == 0.25:
        return {'push': integral, 'exceed': integral + 0.5, 'function': quarter_line_half_loss}
    elif fractional == 0.5:
        return {'exceed': integral + 0.5, 'push': integral + 0.5, 'function': half_or_whole_line}
    elif fractional == 0.75:
        return {'exceed': integral + 0.5, 'push': integral + 1.0, 'function': quarter_line_half_win}
    else:
        raise Exception(f"Unsupported fractional suffix in {value}")


def quarter_line_half_loss(exceed_probability, push_probability):
    return exceed_probability / (1 - (push_probability/2))


def quarter_line_half_win(exceed_probability, push_probability):
    return (exceed_probability - (push_probability/2)) / (1 - (push_probability/2))


def half_or_whole_line(exceed_probability, push_probability):
    return exceed_probability / (1 - push_probability)


def error(par):
    home_xg = np.exp(par[0])
    away_xg = np.exp(par[1])

    home_sum = away_sum = draw_sum = 0
    nearest_tg_lines = find_nearest_tg_lines(tg_line)
    push_line = nearest_tg_lines['push']
    exceed_line = nearest_tg_lines['exceed']
    function = nearest_tg_lines['function']
    exceed_sum = push_sum = 0

    for i in range(16):
        for j in range(16):
            prob = poisson.pmf(i, home_xg) * poisson.pmf(j, away_xg)
            if i > j:
                home_sum += prob
            elif i < j:
                away_sum += prob
            else:
                draw_sum += prob

            if i + j > exceed_line:
                exceed_sum += prob

            if i + j == push_line:
                push_sum += prob

    overs_sum = function(exceed_sum, push_sum)
    unders_sum = 1 - overs_sum

    print(f"Exceed line is {exceed_line}")
    print(f"Push line is {push_line}")
    print(f"Overs fair probability {overs_sum}")
    print(f"Unders fair probability {unders_sum}")
    print(home_sum)
    print(away_sum)
    print(draw_sum)

    return ((home_sum - HOME_FAIR_PROBABILITY)**2 +
            (away_sum - AWAY_FAIR_PROBABILITY)**2 +
            (draw_sum - DRAW_FAIR_PROBABILITY)**2 +
            (overs_sum - OVER_FAIR_PROBABILITY)**2 +
            (unders_sum - UNDER_FAIR_PROBABILITY)**2)


# Use minimize function from scipy.optimize to find the optimal parameters
result = minimize(error, [0, 0], method='Nelder-Mead')
goals = np.exp(result.x)

print(f"Home: {goals[0]}, Away: {goals[1]}")
print(f"TG: {goals[0] + goals[1]}")
print(f"HCP: {goals[0] - goals[1]}")
