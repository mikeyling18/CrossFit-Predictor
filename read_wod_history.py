from movements import Movements
from workout_types import WodFormat

from alpha_library import get_alphas
import pandas as pd
import numpy as np
import re
import copy

pd.options.mode.chained_assignment = None

df_amrap = pd.read_csv('Data/amrap_wod_memory.csv', names = ['format', 'time_limit', 'score', 'WOD'])
df_fortime = pd.read_csv('Data/fortime_wod_memory.csv', names = ['format', 'score', 'WOD'])
df_roundsfortime = pd.read_csv('Data/roundsfortime_wod_memory.csv', names = ['format', 'rounds', 'score', 'WOD'])
# print(df_amrap)

WOD_str = str()
print(df_amrap.iloc[0])
wod_format = df_amrap.iloc[0].format
wod_time = df_amrap.iloc[0].time_limit
wod_score = df_amrap.iloc[0].score
WOD_str = df_amrap.iloc[0].WOD
WOD_str = WOD_str.split('|')[0:-1]


reps_per_set_tuple = list()
wod_tuple = list()
movement_tuple = list()

for object in WOD_str:
    reps = int(re.sub("[a-z]+|\s", "", object))
    reps_per_set_tuple.append(int(reps))
    movement = re.sub("\d+|\s", "", object)
    movement_tuple.append((reps,reps, movement))

reps_per_movement_df = pd.DataFrame(movement_tuple)
reps_per_movement_df.columns = ['reps_in_set', 'reps_performed', 'movement']

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
    print(reps_per_movement_df['reps_performed'].iloc[i % num_movements])

    if reps_last_round > reps_per_movement_df['reps_in_set'].iloc[i % num_movements]:
        reps_per_movement_df['reps_performed'].iloc[i % num_movements] += reps_per_movement_df['reps_in_set'].iloc[i % num_movements]
        reps_last_round -= reps_per_movement_df['reps_in_set'].iloc[i % num_movements]
    elif reps_last_round <= reps_per_movement_df['reps_in_set'].iloc[i % num_movements]:
        reps_per_movement_df['reps_performed'].iloc[i % num_movements] += reps_last_round
        reps_last_round = 0
    i += 1


# find error in current alphas
movements = reps_per_movement_df['movement']
alphas_df = get_alphas()
count = np.array(alphas_df['movement'].isin(movements))
if count == num_movements:
    # you have all movements' alphas, and now you can train/predict
    
print('hi')



