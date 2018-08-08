from workout_types import WodFormat

from alpha_library import get_alphas
import pandas as pd
import numpy as np
import re
import copy
from predict import predict_score
from string import digits

pd.options.mode.chained_assignment = None

df_amrap = pd.read_csv('Data/amrap_wod_memory.csv', names = ['format', 'time_limit', 'score', 'WOD'])
df_fortime = pd.read_csv('Data/fortime_wod_memory.csv', names = ['format', 'score', 'WOD'])
df_roundsfortime = pd.read_csv('Data/roundsfortime_wod_memory.csv', names = ['format', 'rounds', 'score', 'WOD'])
# print(df_amrap)

WOD_str = str()
k = 2
print(df_amrap.iloc[k])
wod_format = df_amrap.iloc[k].format
wod_time = df_amrap.iloc[k].time_limit
wod_score = df_amrap.iloc[k].score
WOD_str = df_amrap.iloc[k].WOD
WOD_str = WOD_str.split('|')[0:-1]


reps_per_set_tuple = list()
wod_tuple = list()
movement_tuple = list()

for object in WOD_str:
    object = object.strip()
    reps = int(re.search('[0-9]+', object).group())
    reps_per_set_tuple.append(int(reps))
    movement = re.sub("\d+|\s", "", object)
    if 'run' in movement:
        movement = object.lstrip(digits)
        movement = re.sub("\s+", "", movement)

    movement_tuple.append((reps,reps, movement))

reps_per_movement_df = pd.DataFrame(movement_tuple)
reps_per_movement_df.columns = ['reps_in_set', 'reps_performed', 'movement']
reps_per_movement_df['alpha'] = 0

reps_per_movement_tuple = copy.deepcopy(movement_tuple)
wod_tuple = (wod_format, wod_time, wod_score, movement_tuple)

reps_per_round = sum(reps_per_set_tuple)
rounds_complete = int(wod_score / reps_per_round)
reps_last_round = wod_score % reps_per_round
reps_per_set = reps_per_set_tuple

reps_per_movement_df['reps_performed'] = reps_per_movement_df['reps_performed'] * rounds_complete
i=0
num_movements = reps_per_movement_df.shape[0]


while reps_last_round > 0:
    # print(reps_per_movement_df['reps_performed'].iloc[i % num_movements])

    if reps_last_round > reps_per_movement_df['reps_in_set'].iloc[i % num_movements]:
        reps_per_movement_df['reps_performed'].iloc[i % num_movements] += reps_per_movement_df['reps_in_set'].iloc[i % num_movements]
        reps_last_round -= reps_per_movement_df['reps_in_set'].iloc[i % num_movements]
    elif reps_last_round <= reps_per_movement_df['reps_in_set'].iloc[i % num_movements]:
        reps_per_movement_df['reps_performed'].iloc[i % num_movements] += reps_last_round
        reps_last_round = 0
    i += 1


# find error in current alphas
movements = reps_per_movement_df['movement'].values
alphas_df = get_alphas()
alpha_list = list()
count = np.sum(np.array(alphas_df['movement'].isin(movements)))

wod_times_list = list()
error_list = list()

# you have all movements' alphas, and now you can train/predict
if count == num_movements:
    for movement in movements:
        print(movement)
        alpha_temp = float(alphas_df.loc[alphas_df['movement'] == movement]['alpha'])
        reps_per_movement_df.loc[reps_per_movement_df['movement'] == movement,'alpha'] = alpha_temp
        # temp_df = alphas_df.loc[alphas_df['movement'].isin(movements)]['alpha'].tolist()
    # reps_per_movement_df = reps_per_movement_df.assign(alpha = temp_df)
    predicted_score = predict_score(reps_per_movement_df, wod_time)
    error = wod_score - predicted_score
    wod_times_list.append(wod_time)
    error_list.append(error)


# you're only missing ONE movement's alpha, so you can calculate a base alpha value
# elif count == num_movements - 1:

print('hi')



