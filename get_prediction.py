import pandas as pd
import re
from predict import predict_score
from string import digits
from get_wod import add_wod_to_memory
from read_amrap_wod_history import read_wods

# below gets rid of 'SettingWithCopyWarning' warning
pd.options.mode.chained_assignment = None

def new_wod_prediction():
    wod_df, wod_time = add_wod_to_memory(new_wod=True)
    alpha_df = pd.read_csv('Data/alpha_library.csv', names=['movement', 'alpha'])

    df_tuple = list()

    WOD_str_pre = wod_df.iloc[0].WOD
    WOD_str = WOD_str_pre.split('|')[0:-1]

    for object in WOD_str:
        object = object.strip()
        reps = int(re.search('[0-9]+', object).group())
        movement = re.sub("\d+|\s", "", object)
        if 'run' in movement:
            movement = object.lstrip(digits)
            movement = re.sub("^\s", "", movement)
        alpha_temp = float(alpha_df.loc[alpha_df['movement'] == movement]['alpha'])
        df_tuple.append((reps, movement, alpha_temp))

    prediction_df = pd.DataFrame(df_tuple)
    prediction_df.columns = ['reps_in_set', 'movement', 'alpha']
    predicted_score = predict_score(prediction_df, wod_time)
    print('Predicted Score: {}\n'.format(predicted_score))

    actual_score = int(input('What did you actually get?\n'))
    wod_df['score'] = [actual_score]
    read_wods(wod_df, new_wod_bool=True)

new_wod_prediction()

