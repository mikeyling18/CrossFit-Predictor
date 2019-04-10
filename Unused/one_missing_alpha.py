from sympy.solvers import solve
from sympy import Symbol
from Unused import alpha_library
import numpy as np
import re


def solve_alpha(wod_df, wod_time, wod_score, unknown_movement, reps_per_round):
    T = wod_time * 60
    Rr = reps_per_round
    Rtot = wod_score
    Ru = wod_df.loc[wod_df['alpha'] == 0.0, 'reps_in_set']

    known_alphas = wod_df.loc[wod_df['alpha'] != 0.0]
    constant = np.sum(known_alphas['alpha'] * known_alphas['reps_in_set'])
    b = (T*Rr/Rtot) - constant

    new_alpha = Symbol('new_alpha')
    alpha_result = float(solve(Ru * new_alpha - b)[new_alpha])
    print(alpha_result)
    new_movement_entry = re.sub('[^a-zA-Z]+', '', str(unknown_movement))
    print('alpha of new movement: ', new_movement_entry, ' is: ', alpha_result)
    alpha_library.update_alpha_library(new_movement_entry, alpha_result)
    print('end of alpha find!')