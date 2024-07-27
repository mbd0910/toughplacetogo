import numpy as np
from scipy.optimize import minimize
from scipy.stats import poisson

# Define initial odds
HOME = 2.46
AWAY = 3.05
DRAW = 3.7

# Convert odds to probabilities
total_sum = 1/HOME + 1/AWAY + 1/DRAW
HOME = 1/HOME/total_sum
AWAY = 1/AWAY/total_sum
DRAW = 1/DRAW/total_sum

tg_line = 2.5
OVER = 1.74
UNDER = 2.26
total_sum = 1/OVER + 1/UNDER
OVER = 1/OVER/total_sum
UNDER = 1/UNDER/total_sum


def error(par):
    homeXG = np.exp(par[0])
    awayXG = np.exp(par[1])

    home_sum = away_sum = draw_sum = overs_sum = unders_sum = 0
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

    return ((home_sum - HOME)**2 +
            (away_sum - AWAY)**2 +
            (draw_sum - DRAW)**2 +
            (overs_sum - OVER)**2 +
            (unders_sum - UNDER)**2)


# Use minimize function from scipy.optimize to find the optimal parameters
result = minimize(error, [0, 0], method='Nelder-Mead')
goals = np.exp(result.x)

print(f"Home: {goals[0]}, Away: {goals[1]}")
