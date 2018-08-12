from scipy.optimize import minimize
import numpy as np

def get_pullups_pushups_squats(cindy_score, angie_score, barbara_score):
    b = (1.0, 3.0)
    bounds = (b, b, b)
    x0 = [1.5, 2.0, 2.0]

    def objective2(x):
        pullups = x[0]
        pushups = x[1]
        squats = x[2]
        return abs(1200 - (cindy_score[0] * pullups + cindy_score[1] * pushups + cindy_score[2] * squats))

    def objective3(x):
        pullups = x[0]
        pushups = x[1]
        squats = x[2]
        return abs(angie_score - (100 * pullups + 100 * pushups + 100 * squats))

    def objective4(x):
        pullups = x[0]
        pushups = x[1]
        squats = x[2]
        return abs(barbara_score - (100 * pullups + 150 * pushups + 250 * squats))

    z = minimize(objective2, x0, method = 'SLSQP', bounds = bounds)
    z1 = z['x']

    z = minimize(objective3, x0, method = 'SLSQP', bounds = bounds)
    z2 = z['x']

    z = minimize(objective4, x0, method = 'SLSQP', bounds = bounds)
    z3 = z['x']

    sol_array2 = np.array([z1,z2,z3])
    print(sol_array2)
    sol_array2 = np.mean(sol_array2, axis = 0)
    alpha_pullups = sol_array2[0]
    alpha_pushups = sol_array2[1]
    alpha_squats = sol_array2[2]
    return alpha_pullups, alpha_pushups, alpha_squats