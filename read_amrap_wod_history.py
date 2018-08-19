import pandas as pd
import numpy as np
import re
from predict import predict_score
from string import digits
from adjust_alpha import change_alphas

pd.options.mode.chained_assignment = None



def read_wods(new_wod_df, new_wod_bool):
    if new_wod_bool is False:
        df_amrap = pd.read_csv('Data/amrap_wod_memory.csv', names = ['format', 'time_limit', 'score', 'WOD'])
    else:
        df_amrap = new_wod_df
    alpha_df = pd.read_csv('Data/alpha_library.csv', names = ['movement', 'alpha'])

    wod_times_list = list()
    error_list = list()

    for k in range(0,df_amrap.shape[0]):
        wod_time = df_amrap.iloc[k].time_limit
        wod_score = df_amrap.iloc[k].score
        wod_str = df_amrap.iloc[k].WOD
        wod_str = wod_str.split('|')[0:-1]


        reps_per_set_tuple = list()
        movement_tuple = list()

        for object in wod_str:
            object = object.strip()
            reps = int(re.search('[0-9]+', object).group())
            reps_per_set_tuple.append(int(reps))
            movement = re.sub("\d+|\s", "", object)
            if 'run' in movement:
                movement = object.lstrip(digits)
                movement = re.sub("^\s", "", movement)
            alpha_temp = float(alpha_df.loc[alpha_df['movement'] == movement]['alpha'])
            movement_tuple.append((reps,reps, movement, alpha_temp))

        reps_per_movement_df = pd.DataFrame(movement_tuple)
        reps_per_movement_df.columns = ['reps_in_set', 'reps_performed', 'movement', 'alpha']
        reps_per_round = sum(reps_per_set_tuple)
        rounds_complete = int(wod_score / reps_per_round)
        reps_last_round = wod_score % reps_per_round

        reps_per_movement_df['reps_performed'] = reps_per_movement_df['reps_performed'] * rounds_complete
        i=0
        num_movements = reps_per_movement_df.shape[0]

        # Determine how many reps were completed in the last round of the workout
        while reps_last_round > 0:
            if reps_last_round > reps_per_movement_df['reps_in_set'].iloc[i % num_movements]:
                reps_per_movement_df['reps_performed'].iloc[i % num_movements] += reps_per_movement_df['reps_in_set'].iloc[i % num_movements]
                reps_last_round -= reps_per_movement_df['reps_in_set'].iloc[i % num_movements]
            elif reps_last_round <= reps_per_movement_df['reps_in_set'].iloc[i % num_movements]:
                reps_per_movement_df['reps_performed'].iloc[i % num_movements] += reps_last_round
                reps_last_round = 0
            i += 1

        movements = np.array(np.unique(reps_per_movement_df['movement'].values))
        movements_in_alpha_library = alpha_df['movement'][alpha_df['movement'].isin(movements)].values
        movements_not_in_alpha_library = set(movements) ^ set(movements_in_alpha_library)

        # you have all movements' alphas, and now you can train/predict
        if len(movements_not_in_alpha_library) == 0:
            predicted_score_old_alphas = predict_score(reps_per_movement_df, wod_time)
            error_old_alphas = (predicted_score_old_alphas - wod_score) / wod_score
            new_alphas = change_alphas(reps_per_movement_df, wod_score, error_old_alphas, wod_time, 0.1)
            temp_df = reps_per_movement_df.copy()
            temp_df['alpha'] = new_alphas
            reps_per_movement_df_new_alphas = temp_df
            predicted_score_new_alpha = predict_score(reps_per_movement_df_new_alphas, wod_time)

            error_new_alphas = (predicted_score_new_alpha - wod_score) / wod_score
            wod_times_list.append(wod_time)

            print('old alpha error: {}\n'
                  'old alpha predicted score: {}\n'
                  'new alpha error: {}\n'
                  'new alpha predicted score: {}\n'
                  'actual score: {}\n'.format(error_old_alphas, predicted_score_old_alphas, error_new_alphas, predicted_score_new_alpha, wod_score))

            # adjust the alpha_df with new alpha values
            for movement in movements:
                alpha_temp = float(np.mean(temp_df.loc[temp_df['movement'] == movement]['alpha']))
                alpha_df.loc[alpha_df['movement'] == movement, 'alpha'] = alpha_temp


    file = open('Data/alpha_library.csv','w')
    file.truncate()
    file = open('Data/alpha_library.csv', 'a')
    for index, row in alpha_df.iterrows():
        file.write('{}, {}\n'.format(row['movement'], row['alpha']))
    file.close()

    # error_vs_time_df = pd.DataFrame({'WOD Time':wod_times_list, 'Error': error_list})

    print('hi')



