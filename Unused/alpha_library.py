import pandas as pd

alpha_df = pd.read_csv('Data/alpha_library.csv', names = ['movement', 'alpha'])


def update_alpha_library(movement, alpha):
    file = open('Data/alpha_library.csv', 'a')
    file.write('{}, {}\n'.format(movement, alpha))
