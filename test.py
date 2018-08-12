import numpy as np
import pandas as pd
from sympy import Symbol
from sympy.solvers.inequalities import solve_rational_inequalities
from scipy.optimize import minimize

import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt

def objective(x):
    pullups = x[0]
    pushups = x[1]
    squats = x[2]
    return (pullups + pushups + squats)

def constraint1(x):
    pullups = x[0]
    pushups = x[1]
    squats = x[2]
    return 1200 - (120*pullups + 235*pushups + 345*squats)

def constraint2(x):
    pullups = x[0]
    pushups = x[1]
    squats = x[2]
    return 880.6 - (100*pullups + 100*pushups + 100*squats)

def constraint3(x):
    pullups = x[0]
    pushups = x[1]
    squats = x[2]
    return 1261.33 - (100*pullups + 150*pushups + 250*squats)

b = (1.0, 3.0)
bounds = (b,b,b)

con1 = {'type': 'eq', 'fun': constraint1}
con2 = {'type': 'eq', 'fun': constraint2}
con3 = {'type': 'eq', 'fun': constraint3}
cons = [con1, con2, con3]
x0 = [1.5, 2.0, 2.0]
sol_array = np.zeros([1,3])
for i in range(0,3):
    sol = minimize(objective, x0, method = 'SLSQP', bounds = bounds, constraints = cons[i])
    y = np.array(sol['x']).reshape([1,3])
    sol_array = np.append(sol_array, y, axis = 0)

sol_array = np.delete(sol_array,(0), axis = 0)
print(sol_array)
sol_array =  np.mean(sol_array, axis = 0)



def objective2(x):
    pullups = x[0]
    pushups = x[1]
    squats = x[2]
    return abs(1200 - (120*pullups + 235*pushups + 345*squats))

def objective3(x):
    pullups = x[0]
    pushups = x[1]
    squats = x[2]
    return abs(880.6 - (100*pullups + 100*pushups + 100*squats))

def objective4(x):
    pullups = x[0]
    pushups = x[1]
    squats = x[2]
    return abs(1261.33 - (100*pullups + 150*pushups + 250*squats))

z = minimize(objective2, x0, method = 'SLSQP', bounds = bounds)
z1 = z['x']

z = minimize(objective3, x0, method = 'SLSQP', bounds = bounds)
z2 = z['x']

z = minimize(objective4, x0, method = 'SLSQP', bounds = bounds)
z3 = z['x']

sol_array2 = np.array([z1,z2,z3])
print(sol_array2)
sol_array2 = np.mean(sol_array2, axis = 0)

wods = [[120, 235, 245],[100,100,100],[100,150,250]]
result1 = np.matmul(wods, sol_array)
print('\n')
result2 = np.matmul(wods, sol_array2)
combined_alphas = np.array([sol_array, sol_array2])
combined_alphas = np.mean(combined_alphas, axis = 0)

combined_results = np.matmul(wods,combined_alphas)
actual_results = [1200, 880, 1261]
error1 = (result1 - actual_results)/actual_results
error2 = (result2 - actual_results)/actual_results
combined_error = (combined_results - actual_results) / actual_results

print('error1 - {}'.format(error1))
print('error2 - {}'.format(error2))
print(combined_error)

reps_set = [5,10,15, 100,100,100, 20,30,50]
alpha_list = list(np.array([z1,z2,z3]).reshape(9,))

plt.plot(reps_set, alpha_list, 'ro')
plt.axis([0,120,0,3])
plt.show()