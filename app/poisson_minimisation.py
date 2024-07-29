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

tg_line = 3.0
OVER_BOOKIE_ODDS = 2.39
UNDER_BOOKIE_ODDS = 1.67
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

def error(par):
    homeXG = np.exp(par[0])
    awayXG = np.exp(par[1])

    home_sum = away_sum = draw_sum = overs_sum = unders_sum = 0
    exact_line = 0
    for i in range(16):
        for j in range(16):
            prob = poisson.pmf(i, homeXG) * poisson.pmf(j, awayXG)
            if i > j:
                home_sum += prob
            elif i < j:
                away_sum += prob
            else:
                draw_sum += prob

            if i + j > tg_line:
                overs_sum += prob
            elif i + j < tg_line:
                unders_sum += prob
            else:
                exact_line += prob

    print(f"Overs sum {overs_sum}")
    print(f"Unders sum {unders_sum}")
    print(f"Exact prob {exact_line}")

    overs_odds = (1 - exact_line) / overs_sum
    unders_odds = (1 - exact_line) / unders_sum

    print(f"Overs odds {overs_odds}")
    print(f"Unders odds {unders_odds}")
    overs_fp = 1 / overs_odds
    unders_fp = 1 / unders_odds
    print(f"Overs fair probability {overs_fp}")
    print(f"Unders fair probability {unders_fp}")
    print(home_sum)
    print(away_sum)
    print(draw_sum)

    return ((home_sum - HOME_FAIR_PROBABILITY)**2 +
            (away_sum - AWAY_FAIR_PROBABILITY)**2 +
            (draw_sum - DRAW_FAIR_PROBABILITY)**2 +
            (overs_fp - OVER_FAIR_PROBABILITY)**2 +
            (unders_fp - UNDER_FAIR_PROBABILITY)**2)


# Use minimize function from scipy.optimize to find the optimal parameters
result = minimize(error, [0, 0], method='Nelder-Mead')
goals = np.exp(result.x)

print(f"Home: {goals[0]}, Away: {goals[1]}")
print(f"TG: {goals[0] + goals[1]}")
print(f"HCP: {goals[0] - goals[1]}")
