import pandas as pd
import numpy as np
import math


def predict_score(wod_df, wod_time):
    print(wod_df)
    print(wod_time)

    wod_df = wod_df.assign(predicted_reps = 0)
    num_components = wod_df.shape[0]
    t_current = 0.0
    t_since_last_rep = 0.0
    i = 0
    wod_time_seconds = wod_time * 60


    wod_component = wod_df.iloc[i % num_components]
    reps_in_set = wod_component['reps_in_set']
    reps_completed_current_set = 0
    alpha = wod_component['alpha']
    # gamma = math.sqrt((math.log10(wod_time) * (wod_time_seconds + t_current) / wod_time_seconds ) / math.log10(wod_time))
    while t_current < wod_time_seconds:
        # alpha = alpha * gamma
        if t_since_last_rep >= alpha:
            wod_df['predicted_reps'].iloc[i % num_components] += 1
            reps_completed_current_set += 1
            t_since_last_rep = 0
            # alpha = alpha * gamma

        if reps_completed_current_set == reps_in_set:
            reps_completed_current_set = 0
            i += 1
            wod_component = wod_df.iloc[i % num_components]
            reps_in_set = wod_component['reps_in_set']
            alpha = wod_component['alpha']


        # wod_df[].iloc[i % num_movements])
        t_current += 0.1
        t_since_last_rep += 0.1
        # gamma = math.sqrt((math.log10(wod_time) * (wod_time_seconds + t_current) / wod_time_seconds) / math.log10(wod_time))

    predicted_score = np.sum(wod_df['predicted_reps'])
    return predicted_score
    print('hi')