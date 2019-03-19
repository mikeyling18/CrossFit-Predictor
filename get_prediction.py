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


def parse_wod(wod_str, alpha_df):
    """
    Description
    -----------
    Break down the wod_str object and create a list that contains (reps, movement, alpha) for each movement described
    in the WOD


    :param wod_str: string
        contains information for each movement in the WOD. For example '15 snatches 135' means 15 repetitions of the
        snatch at 135 lbs.
    :param alpha_df: Dataframe
        the master dataframe of ALL alpha values for all movements

    :return df_tuple : list[tuple]
        each tuple has the following information (reps, movement, alpha). This information is extracted from each
        movement in the wod_str. For example, '15 snatches 135' would yield a tuple of (15, snatches, alpha for snatches)

    Notes
    -----
    Calculated alpha values for movements that involve weights, like snatches and clean and jerks, is done in a linear
    fashion. For example, the default weight of a snatch is 135lbs (stored in variable DEFAULT_SNATCH_WEIGHT). So,
    if the workout calls for snatches at 95 lbs, then the alpha for the snatch is now 95/135 * alpha.
    """
    df_tuple = list()

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

    return df_tuple


def new_wod_prediction():
    """
    Description
    -----------
    Coordinates all the proper method calls to enter a new WOD and get a prediction by calling the following functions:
        - add_wod_to_memory()
        - predict_score()
    Proper descriptions of the methods can be found where they are defined


    Important Variable Descriptions
    -------------------------------

    wod_obj will have the following components based on the type of workout entered:
        -AMRAP:
            wod_obj = List[wod_format, wod_df, wod_time]
                wod_format : enum
                    Determines which type of WOD the workout is
                wod_df : Dataframe
                    format        : score : WOD
                    RoundsForTime : 120   : 15 pushups|10 pullups|
                wod_time : string
                    Represents the amount of time alloted for the AMRAP in mm:ss format

        -RoundsForTime:
            wod_obj = List[wod_format, wod_df, rounds]
                wod_format : enum
                    Determines which type of WOD the workout is
                wod_df : Dataframe
                    format        : score : WOD
                    RoundsForTime : 120   : 15 pushups|10 pullups|
                rounds : int
                    The number of rounds that need to be completed in the WOD



    Returns
    -------
    None, but .csv files are used to store the new WOD and its results. The csv files have different formats depending
    on the format of the WOD:
        -AMRAPs -> wod format, time alloted, score, wod description
        -RoundsForTime -> wod format, rounds, score, wod description

    """
    wod_obj = add_wod_to_memory(new_wod=True)
    wod_format = wod_obj[0]
    alpha_df = pd.read_csv('Data/alpha_library.csv', names=['movement', 'alpha'])


    # If the new WOD is an AMRAP:
    if wod_format == WodFormat.AMRAP:
        wod_df = wod_obj[1]
        wod_time = wod_obj[2]
        wod_str_pre = wod_df.iloc[0].WOD
        wod_str = wod_str_pre.split('|')[0:-1]

        df_tuple = parse_wod(wod_str, alpha_df)

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

        df_tuple = parse_wod(wod_str, alpha_df)

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
        read_wods(wod_format, wod_df, new_wod_bool=True)
        file = open('Data/rft_wod_memory.csv', 'a')
        file.write('{}, {}, {}, {}\n'.format(wod_df.format[0], rounds, actual_score, wod_str_pre))

if __name__ == "__main__":
    new_wod_prediction()

