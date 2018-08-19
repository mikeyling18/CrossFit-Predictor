import numpy as np
import pandas as pd
from sympy import Symbol
from sympy.solvers.inequalities import solve_rational_inequalities
from scipy.optimize import minimize

import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt

movement_df = pd.read_csv('Data/movement_reps_and_alphas/snatches.csv', names=['reps_in_set', 'alpha'])
alphas = np.array(movement_df['alpha'])
reps_in_set_values = np.array(movement_df['reps_in_set'])
coefficients = np.polyfit(np.log(reps_in_set_values), alphas, 1)

print('Regression line for {}: {}log(x) + {}\n'.format('snatches', coefficients[0], coefficients[1]))

x_limits = np.linspace(0,35)
y = coefficients[0] * np.log(x_limits) + coefficients[1]

plt.plot(x_limits, y, '--', label='fit')
plt.plot(reps_in_set_values, alphas, 'o', label='data')
plt.legend()
plt.show()

# plt.plot(x,y,"o",label="data")
# plt.plot(x,fit(np.log(x)),"--", label="fit")
