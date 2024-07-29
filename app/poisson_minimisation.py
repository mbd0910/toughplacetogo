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
        return integral, integral
    elif fractional == 0.25:
        return integral, integral + 0.5
    elif fractional == 0.5:
        return integral + 0.5, integral + 0.5
    elif fractional == 0.75:
        return integral + 0.5, integral + 1.0
    else:
        raise Exception(f"Unsupported fractional suffix in {value}")

def error(par):
    homeXG = np.exp(par[0])
    awayXG = np.exp(par[1])

    home_sum = away_sum = draw_sum = 0
    nearest_tg_lines = find_nearest_tg_lines(tg_line)
    tg_line_totals = {
        nearest_tg_lines[0]: {
            'overs_sum': 0,
            'unders_sum': 0,
            'exact_line_sum': 0
        },
        nearest_tg_lines[1]: {
            'overs_sum': 0,
            'unders_sum': 0,
            'exact_line_sum': 0
        }
    }

    for i in range(16):
        for j in range(16):
            prob = poisson.pmf(i, homeXG) * poisson.pmf(j, awayXG)
            if i > j:
                home_sum += prob
            elif i < j:
                away_sum += prob
            else:
                draw_sum += prob

            for line, totals in tg_line_totals.items():
                if i + j > line:
                    totals['overs_sum'] += prob
                elif i + j < line:
                    totals['unders_sum'] += prob
                else:
                    totals['exact_line_sum'] += prob

    overs_sum = unders_sum = 0
    print(tg_line_totals)

    for line, totals in tg_line_totals.items():
        overs_sum += totals['overs_sum'] / (1 - totals['exact_line_sum'])
        unders_sum += totals['unders_sum'] / (1 - totals['exact_line_sum'])

    overs_sum /= len(tg_line_totals)
    unders_sum /= len(tg_line_totals)

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
