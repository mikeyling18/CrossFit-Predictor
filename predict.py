import pandas as pd
import numpy as np
import math
import re
from string import digits
import copy
from workout_types import WodFormat

def get_seconds(time_str):
    m,s = time_str.split(':')
    return int(m) * 60 + int(s)

'''
This function gets the predicted score of the WOD. 
It behaves differently depending on the workout type

Input: List, wod_format
    If wod_format = AMRAP, List = [wod_df, wod_time]
    If wod_format = RoundsForTime, List = [wod_df]
Output: predicted_score

wod_df is a dataframe that has the following columns: 
[reps_in_set : movement : alpha]
'''
def predict_score(wod_obj, wod_format):
    if wod_format == WodFormat.AMRAP:
        wod_df = wod_obj[0]
        wod_time = wod_obj[1]

        wod_df = wod_df.assign(predicted_reps=0)

        wod_time_seconds = get_seconds(wod_time)
        num_components = wod_df.shape[0]

        t_current = 0.0
        t_since_last_rep = 0.0
        i = 0

        total_seconds_per_round = np.sum(wod_df['reps_in_set'] * wod_df['alpha'])
        whole_rounds_complete = int(wod_time_seconds / total_seconds_per_round)
        seconds_in_last_round = wod_time_seconds % total_seconds_per_round

        wod_component = wod_df.iloc[i % num_components]
        reps_in_set = wod_component['reps_in_set']
        reps_completed_current_set = 0
        alpha = wod_component['alpha']
        while t_current < seconds_in_last_round:
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

        whole_rounds_reps = whole_rounds_complete * np.sum(wod_df['reps_in_set'])
        last_round_reps = np.sum(wod_df['predicted_reps'])
        predicted_score = whole_rounds_reps + last_round_reps
        return predicted_score

    elif wod_format == WodFormat.RoundsForTime:
        wod_df = wod_obj[0]
        rounds = int(wod_obj[1])
        wod_df = wod_df.assign(predicted_reps=0)
        num_components = wod_df.shape[0]

        i = 0
        completed_reps = 0
        t_since_last_rep = 0.0
        t_current = 0.0
        total_reps = rounds * np.sum(wod_df['reps_in_set'])
        reps_completed_current_set = 0

        wod_component = wod_df.iloc[i % num_components]
        reps_in_set = wod_component['reps_in_set']
        alpha = wod_component['alpha']

        while completed_reps < total_reps:
            if t_since_last_rep >= alpha:
                wod_df['predicted_reps'].iloc[i % num_components] += 1
                reps_completed_current_set += 1
                completed_reps += 1
                t_since_last_rep = 0.0
            if reps_completed_current_set == reps_in_set:
                reps_completed_current_set = 0
                i += 1
                wod_component = wod_df.iloc[i % num_components]
                reps_in_set = wod_component['reps_in_set']
                alpha = wod_component['alpha']
            t_current += 0.1
            t_since_last_rep += 0.1

        return t_current
