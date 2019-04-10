from scipy.optimize import minimize
import numpy as np


def get_pullups_pushups_squats(cindy_score, angie_score, barbara_score):
    """
    This is a specially made function to get the alpha values for an athlete's pullups, pushups, and squats.

    :param cindy_score: int
    :param angie_score: str
    :param barbara_score: str
    :return: float, float, float - alpha_pullups, alpha_pushups, alpha_squats
    """
    b = (1.0, 3.0)
    bounds = (b, b, b)
    x0 = [1.5, 2.0, 2.0]

    def objective1(x):
        pullups = x[0]
        pushups = x[1]
        squats = x[2]
        return abs(1200 - (cindy_score[0] * pullups + cindy_score[1] * pushups + cindy_score[2] * squats))

    def objective2(x):
        pullups = x[0]
        pushups = x[1]
        squats = x[2]
        return abs(angie_score - (100 * pullups + 100 * pushups + 100 * squats))

    def objective3(x):
        pullups = x[0]
        pushups = x[1]
        squats = x[2]
        return abs(barbara_score - (100 * pullups + 150 * pushups + 250 * squats))

    z = minimize(objective1, x0, method = 'SLSQP', bounds = bounds)
    z1 = z['x']
    cindy_pullup_alpha = z1[0]
    cindy_pushup_alpha = z1[1]
    cindy_squat_alpha = z1[2]

    z = minimize(objective2, x0, method = 'SLSQP', bounds = bounds)
    z2 = z['x']
    angie_pullup_alpha = z2[0]
    angie_pushup_alpha = z2[1]
    angie_squat_alpha = z2[2]

    z = minimize(objective3, x0, method = 'SLSQP', bounds=bounds)
    z3 = z['x']
    barbara_pullup_alpha = z3[0]
    barbara_pushup_alpha = z3[1]
    barbara_squat_alpha = z3[2]

    file = open('Data/movement_reps_and_alphas/pullups.csv', 'a')
    file.write('{},{}\n'
               '{},{}\n'.format(5, cindy_pullup_alpha,
                                100, angie_pullup_alpha))

    file = open('Data/movement_reps_and_alphas/pushups.csv', 'a')
    file.write('{},{}\n'
               '{},{}\n'.format(10, cindy_pushup_alpha,
                                100, angie_pushup_alpha))

    file = open('Data/movement_reps_and_alphas/squats.csv', 'a')
    file.write('{},{}\n'
               '{},{}\n'.format(15, cindy_squat_alpha,
                                100, angie_squat_alpha))

    sol_array2 = np.array([z1,z2,z3])
    print(sol_array2)
    sol_array2 = np.mean(sol_array2, axis = 0)
    alpha_pullups = sol_array2[0]
    alpha_pushups = sol_array2[1]
    alpha_squats = sol_array2[2]
    return alpha_pullups, alpha_pushups, alpha_squats
