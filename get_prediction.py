import pandas as pd
import re
from predict import predict_score
from string import digits
from get_wod import add_wod_to_memory
from read_amrap_wod_history import read_wods
from workout_types import WodFormat
from default_values import *

# below gets rid of 'SettingWithCopyWarning' warning
pd.options.mode.chained_assignment = None


def new_wod_prediction():
    #wod_obj will have the following components based on the type of workout entered:
    # AMRAP:
    # wod_obj = List[wod_format, wod_df, wod_time]
    #
    # RoundsForTime:
    # wod_obj = List[wod_format, wod_df]

    # wod_df is a dataframe that contains all the necessary information for a WOD:
    # format        : score : WOD
    # RoundsForTime : 120   : 15 pushups|10 pullups|

    wod_obj = add_wod_to_memory(new_wod=True)

    # Get the format of the WOD. We handle the wod_obj differently depending on the format of the WOD
    wod_format = wod_obj[0]

    alpha_df = pd.read_csv('Data/alpha_library.csv', names=['movement', 'alpha'])

    df_tuple = list()

    # If the new WOD is an AMRAP:
    if wod_format == WodFormat.AMRAP:
        wod_df = wod_obj[1]
        wod_time = wod_obj[2]
        wod_str_pre = wod_df.iloc[0].WOD
        wod_str = wod_str_pre.split('|')[0:-1]

        for object in wod_str:
            object = object.strip()
            reps = int(re.search('[0-9]+', object).group())
            movement = re.sub("\d+|\s", "", object)

            if 'run' in movement:
                movement = object.lstrip(digits)
                movement = re.sub("^\s", "", movement)
            alpha_temp = float(alpha_df.loc[alpha_df['movement'] == movement]['alpha'])
            if 'snatch' in movement:
                weight = int(re.search('\d+$', object).group())
                ratio = weight / DEFAULT_SNATCH_WEIGHT
                alpha_temp *= ratio
            df_tuple.append((reps, movement, alpha_temp))

        prediction_df = pd.DataFrame(df_tuple)
        prediction_df.columns = ['reps_in_set', 'movement', 'alpha']
        predicted_score = predict_score([prediction_df, wod_time], wod_format)

        scoreReveal = input("When would you like to see your predicted score? (now/after)\n")
        if scoreReveal == 'now':
            print('Predicted Score: {}\n'.format(predicted_score))
            actual_score = int(input('What was your score?\n'))
        else:
            actual_score = int(input('What was your score?\n'))
            print('Predicted Score: {}\n'.format(predicted_score))
        wod_df['score'] = [actual_score]
        read_wods(wod_format, wod_df, new_wod_bool=True)
        file = open('Data/amrap_wod_memory.csv', 'a')
        file.write('{}, {}, {}, {}\n'.format(wod_df.format[0], wod_time, actual_score, wod_str_pre))

    elif wod_format == WodFormat.RoundsForTime:
        wod_df = wod_obj[1]
        rounds = wod_obj[2]
        wod_str_pre = wod_df.iloc[0].WOD
        wod_str = wod_str_pre.split('|')[0:-1]

        for object in wod_str:
            object = object.strip()
            reps = int(re.search('[0-9]+', object).group())
            movement = re.sub("\d+|\s", "", object)
            if 'run' in movement:
                movement = object.lstrip(digits)
                movement = re.sub("^\s", "", movement)
            alpha_temp = float(alpha_df.loc[alpha_df['movement'] == movement]['alpha'])
            if 'snatch' in movement:
                weight = int(re.search('\d+$', object).group())
                ratio = weight / DEFAULT_SNATCH_WEIGHT
                alpha_temp *= ratio
            df_tuple.append((reps, movement, alpha_temp))

        prediction_df = pd.DataFrame(df_tuple)
        prediction_df.columns = ['reps_in_set', 'movement', 'alpha']
        predicted_score = predict_score([prediction_df, rounds], wod_format)

        scoreReveal = input("When would you like to see your predicted score? (now/after)\n")
        if scoreReveal == 'now':
            print('Predicted Score: {}\n'.format(predicted_score))
            actual_score = int(input('What was your score?\n'))
        else:
            actual_score = int(input('What was your score?\n'))
            print('Predicted Score: {}\n'.format(predicted_score))
        wod_df['score'] = [actual_score]
        read_wods(wod_df, new_wod_bool=True)
        file = open('Data/rft_wod_memory.csv', 'a')
        file.write('{}, {}, {}, {}\n'.format(wod_df.format[0], rounds, actual_score, wod_str_pre))

if __name__ == "__main__":
    new_wod_prediction()

