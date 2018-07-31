from movements import Movements
from workout_types import WodFormat

import pandas as pd
import numpy as np

df_amrap = pd.read_csv('Data/amrap_wod_memory.csv', names = ['format', 'time_limit', 'score', 'WOD'])
df_fortime = pd.read_csv('Data/fortime_wod_memory.csv', names = ['format', 'score', 'WOD'])
df_roundsfortime = pd.read_csv('Data/roundsfortime_wod_memory.csv', names = ['format', 'rounds', 'score', 'WOD'])
print(df_amrap)