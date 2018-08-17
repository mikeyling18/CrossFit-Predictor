import pandas as pd
import numpy as np
import math

def get_seconds(time_str):
    m,s = time_str.split(':')
    return int(m) * 60 + int(s)

def predict_score(wod_df, wod_time):
    wod_df = wod_df.assign(predicted_reps = 0)
    num_components = wod_df.shape[0]
    t_current = 0.0
    t_since_last_rep = 0.0
    i = 0
    wod_time_seconds = get_seconds(wod_time)


    wod_component = wod_df.iloc[i % num_components]
    reps_in_set = wod_component['reps_in_set']
    reps_completed_current_set = 0
    alpha = wod_component['alpha']
    while t_current < wod_time_seconds:
        if t_since_last_rep >= alpha:
            wod_df['predicted_reps'].iloc[i % num_components] += 1
            reps_completed_current_set += 1
            t_since_last_rep = 0

        if reps_completed_current_set == reps_in_set:
            reps_completed_current_set = 0
            i += 1
            wod_component = wod_df.iloc[i % num_components]
            reps_in_set = wod_component['reps_in_set']
            alpha = wod_component['alpha']

        t_current += 0.1
        t_since_last_rep += 0.1

    predicted_score = np.sum(wod_df['predicted_reps'])
    return predicted_score
    print('hi')