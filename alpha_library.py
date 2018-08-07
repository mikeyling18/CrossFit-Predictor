import pandas as pd

alpha_library = {

}

benchmark_rep_dict = {
    '1600m_run' : 1,
    '2000m_row': 1,
    'wall_ball': 150,
    'clean_and_jerk': 30,
    'snatch': 30,
    'double_under': 200,
    'cal_row': 50
}

def get_alphas():
    df_alphas = pd.read_csv('Data/alpha_library.csv', names = ['movement', 'alpha'])
    return df_alphas