import pandas as pd
import numpy as np
import math
import re
from string import digits
import copy


def get_seconds(time_str):
    m,s = time_str.split(':')
    return int(m) * 60 + int(s)


def get_score(wod_format, wod_time, wod_score, wod_str):
    # wod_format = df_amrap.iloc[k].format
    # wod_time = df_amrap.iloc[k].time_limit
    # wod_score = df_amrap.iloc[k].score
    # WOD_str = df_amrap.iloc[k].WOD
    # WOD_str = WOD_str.split('|')[0:-1]

    reps_per_set_tuple = list()
    wod_tuple = list()
    movement_tuple = list()

    for object in wod_str:
        object = object.strip()
        reps = int(re.search('[0-9]+', object).group())
        reps_per_set_tuple.append(int(reps))
        movement = re.sub("\d+|\s", "", object)
        if 'run' in movement:
            movement = object.lstrip(digits)
            movement = re.sub("^\s", "", movement)

        movement_tuple.append((reps, reps, movement))

    reps_per_movement_df = pd.DataFrame(movement_tuple)
    reps_per_movement_df.columns = ['reps_in_set', 'reps_performed', 'movement']
    reps_per_movement_df['alpha'] = 0

    reps_per_movement_tuple = copy.deepcopy(movement_tuple)
    wod_tuple = (wod_format, wod_time, wod_score, movement_tuple)

    reps_per_round = sum(reps_per_set_tuple)
    rounds_complete = int(wod_score / reps_per_round)
    reps_last_round = wod_score % reps_per_round
    reps_per_set = reps_per_set_tuple


def predict_score(wod_df, wod_time):
    wod_df = wod_df.assign(predicted_reps = 0)
    wod
    num_components = wod_df.shape[0]
    t_current = 0.0
    t_since_last_rep = 0.0
    i = 0
    wod_time_seconds = get_seconds(wod_time)

    total_seconds_per_round = np.sum(wod_df['reps_in_set'] * wod_df['alpha'])
    whole_rounds_complete = int(wod_time_seconds / total_seconds_per_round)
    seconds_in_last_round = wod_time_seconds % total_seconds_per_round


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