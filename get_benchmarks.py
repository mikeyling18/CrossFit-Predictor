import pandas as pd
import numpy as np
import re
import solver
from string import digits

pd.options.mode.chained_assignment = None

alpha_df = pd.DataFrame()

def get_seconds(time_str):
    m,s = time_str.split(':')
    return int(m) * 60 + int(s)

def get_run_times(df, run_time):
    alpha_800 = 2*(run_time/4.0 - 5)
    alpha_400 = alpha_800/2.0 - 5
    alpha_200 = alpha_400/2.0 - 5
    alpha_100 = alpha_200/2.0

    run_dict = {
        '800m run' : alpha_800,
        '400m run' : alpha_400,
        '200m run' : alpha_200,
        '100m run' : alpha_100
    }
    # run_list = list(run_dict.keys())
    for key, value in run_dict.items():
        df = df.append(pd.DataFrame({'movement': [key], 'alpha': [value]}))
    return df

def get_amrap_reps(df_amrap):
    wod_score = int(df_amrap.iloc[0].score)
    WOD_str = df_amrap.iloc[0].WOD
    WOD_str = WOD_str.split('|')[0:-1]


    reps_per_set_tuple = list()
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

    reps_per_round = sum(reps_per_set_tuple)
    rounds_complete = int(wod_score / reps_per_round)
    reps_last_round = wod_score % reps_per_round
    # reps_per_set = reps_per_set_tuple

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

    print('hi')
    return reps_per_movement_df


benchmarks = ['Mile Time', '2k Row', 'Karen (150 Wall Ball For Time', 'Grace (30 C&Js @ 135)',
              'Isabel (30 Snatches @ 135)', '200 Double Unders For Time', '50 Cal Row For Time']
benchmark_names = ['mile', '2krow', 'karen', 'grace', 'isabel', '200du', '50calrow']
alpha_names = ['1600m_run', '2000m_row', 'wallballs', 'cleanandjerks', 'snatches', 'doubleunders', 'calrow']




# Get run-related alphas
mileTime = input('What is your mile time? (mm:ss format)\n')
seconds = get_seconds(mileTime)
alpha_df = alpha_df.append(pd.DataFrame({'movement':['1600m run'], 'alpha':[seconds]}))
alpha_df = get_run_times(alpha_df, seconds)

# Get clean and clean&jerk alphas
graceTime = input('What is your Grace (30 clean and jerks @ 135# for time) time? (mm:ss format)\n')
seconds = get_seconds(graceTime)
cleanjerk_alpha = seconds / 30.0
clean_alpha = cleanjerk_alpha/1.5
alpha_df = alpha_df.append(pd.DataFrame({'movement': ['cleanandjerks', 'cleans'], 'alpha':[cleanjerk_alpha, clean_alpha]}))

# Get snatch alpha
isabelTime = input('What is your Isabel (30 snatch @ 135# for time) time?\n')
seconds = get_seconds(isabelTime)
alpha_snatches = seconds / 30.0
alpha_df = alpha_df.append(pd.DataFrame({'movement': ['snatches'], 'alpha': [alpha_snatches]}))



# Get 2k row alpha
row2kTime = input('What is your 2k Row time?\n')
row2k_alpha = get_seconds(row2kTime)
row1k_alpha = ((row2k_alpha/4.0) - 5.0) * 2
row500m_alpha = row2k_alpha/4.0 - 10.0
alpha_df = alpha_df.append(pd.DataFrame({'movement': ['2000m row', '1000m row', '500m row'], 'alpha': [row2k_alpha, row1k_alpha, row500m_alpha]}))

# Get cal row alpha
row50calTime = input('What is your 50 Calorie Row time?\n')
seconds = get_seconds(row50calTime)
rowcal_alpha = seconds / 50.0
alpha_df = alpha_df.append(pd.DataFrame({'movement': ['calrow'], 'alpha': [rowcal_alpha]}))
#
# Get double under alpha
duTime = input('What is your 200 Double Unders for Time score?\n')
seconds = get_seconds(duTime)
du_alpha = seconds / 200.0
alpha_df = alpha_df.append(pd.DataFrame({'movement': ['doubleunders'], 'alpha': [du_alpha]}))

# Get situps alpha from Annie
annieTime = input('What is your Annie Time? \n 50-40-30-20-10 \n Double-Unders \n Situps\n')
seconds = get_seconds(annieTime)
situps_alpha = (seconds - 150 * du_alpha) / 150.0
alpha_df = alpha_df.append(pd.DataFrame({'movement': ['situps'], 'alpha': [situps_alpha]}))

# Get Pullups, Pushups, and Squats from Cindy, Angie, and Barbara

cindyScore = input('What is your Cindy score?\n'
                   '20 min AMRAP:\n'
                   '5 Pullups\n'
                   '10 Pushups\n'
                   '15 Squats\n')
df_amrap = pd.DataFrame({'format': ['AMRAP'], 'time_limit': [20], 'score': [cindyScore], 'WOD': ['5 pullups|10 pushups|15 squats|']})
reps = get_amrap_reps(df_amrap)
cindy_reps = np.array(reps['reps_performed'])
cindyTime_seconds = get_seconds('20:00')

angieTime = input('What is your Angie time? \n '
                  'For Time: \n'
                  '100 Pullups\n'
                  '100 Pushups\n'
                  '100 Situps \n'
                  '100 Squats\n')
angieTime_seconds = get_seconds(angieTime)
angieTime_seconds = angieTime_seconds - 100 * alpha_df['alpha'].loc[alpha_df['movement'] =='situps']
angie_reps = np.array([100, 100, 100])

barbaraTime = input('What is your Barbara time? (rest included)\n'
                    '20 Pullups \n'
                    '30 Pushups \n'
                    '40 Situps \n'
                    '50 Squats\n '
                    'Rest 3 Minutes Between Each Round\n')
barbaraTime_seconds = get_seconds(barbaraTime)
barbaraTime_seconds = barbaraTime_seconds - get_seconds('12:00') - 200 * alpha_df['alpha'].loc[alpha_df['movement'] == 'situps']
barbara_reps = np.array([100, 150, 250])

alpha_pullups, alpha_pushups, alpha_squats = solver.get_pullups_pushups_squats(cindy_reps, angieTime_seconds, barbaraTime_seconds)
alpha_pistols = 1.4 * alpha_squats
alpha_df = alpha_df.append(pd.DataFrame({'movement': ['pullups', 'pushups', 'squats', 'pistols'], 'alpha': [alpha_pullups, alpha_pushups, alpha_squats, alpha_pistols]}))

# Get Thruster alpha with Fran
franTime = input('What is your Fran Time? \n 21-15-9\n Thrusters @ 95#\n Pullups\n')
fran_seconds = get_seconds(franTime)
thruster_alpha = float((fran_seconds - 45.0 * alpha_df['alpha'].loc[alpha_df['movement'] == 'pullups']) / 45.0)
alpha_df = alpha_df.append(pd.DataFrame({'movement': ['thrusters'], 'alpha': [thruster_alpha]}))

# Get Wallball alpha from Karen
karenTime = input('What is your Karen Time?\n'
                  'For Time:\n'
                  '150 Wallballs @ 20#\n')
karen_seconds = get_seconds(karenTime)
alpha_wallball = karen_seconds / 150.0
alpha_df = alpha_df.append(pd.DataFrame({'movement': ['wallballs'], 'alpha':[alpha_wallball]}))

# Get Boxjumps alpha from Kelly
kellyTime = input('What is your Kelly Time?\n'
                  '5 Rounds for Time:\n'
                  '400m Run\n'
                  '30 Boxjumps @ 24"\n'
                  '30 Wallballs @ 20#\n')
kelly_seconds = get_seconds(kellyTime)
alpha_400mrun = alpha_df['alpha'].loc[alpha_df['movement'] == '400m run']
alpha_wallball = alpha_df['alpha'].loc[alpha_df['movement'] == 'wallballs'] * 0.80
alpha_boxjumps = float((kelly_seconds - 5 * alpha_400mrun - 150 * alpha_wallball) / 150.0)
alpha_df = alpha_df.append(pd.DataFrame({'movement': ['boxjumps'], 'alpha': [alpha_boxjumps]}))

# Get Kettlebell Swings @ 53# with Helen
helenTime = input('What is your Helen Time?\n'
                  '3 Rounds for Time:\n'
                  '400m Run\n'
                  '21 Kettlebell Swings @ 53#\n'
                  '12 Pullups\n')
helen_seconds = get_seconds(helenTime)
alpha_pullups = alpha_df['alpha'].loc[alpha_df['movement'] == 'pullups']
alpha_kbs = float((helen_seconds - 3 * alpha_400mrun - 36 * alpha_pullups) / 63.0)
alpha_df = alpha_df.append(pd.DataFrame({'movement': ['kettlebell swings'], 'alpha': [alpha_kbs]}))

nancyTime = input('What is your Nancy Time?\n'
                  '5 Rounds for Time:\n'
                  '400m Run\n'
                  '15 Overhead Squats @ 95\n')
nancy_seconds = get_seconds(nancyTime)
alpha_ohs = float((nancy_seconds - 5 * alpha_400mrun) / 75.0)
alpha_df = alpha_df.append(pd.DataFrame({'movement': ['overhead squats'], 'alpha': [alpha_ohs]}))

amandaTime = input('What is your Amanda Time?\n'
                   'For Time:\n'
                   '9-7-5 of\n'
                   'Muscle-Ups\n'
                   'Snatches @ 135#\n')
amanda_seconds = get_seconds(amandaTime)
alpha_muscleups = float((amanda_seconds - 21*alpha_snatches) / 21.0)
alpha_df = alpha_df.append(pd.DataFrame({'movement': 'muscleups', 'alpha': [alpha_muscleups]}))

maryScore = input('What is your Mary Score?\n'
                 '20 Minute AMRAP\n'
                 '5 Handstand Pushups\n'
                 '10 Pistols\n'
                 '15 Pullups\n')
df_mary = pd.DataFrame({'format': ['AMRAP'], 'time_limit': [20], 'score': [maryScore], 'WOD': ['5 handstand pushups|10 pistols|15 pullups|']})
reps = get_amrap_reps(df_mary)
hspu_reps = reps['reps_performed'].iloc[0]
pistol_reps = reps['reps_performed'].iloc[1]
pullup_reps = reps['reps_performed'].iloc[2]
alpha_hspu = float( (get_seconds('20:00') - pistol_reps * alpha_pistols - pullup_reps * alpha_pullups) / hspu_reps)
alpha_df = alpha_df.append(pd.DataFrame({'movement': 'handstand pushups', 'alpha': [alpha_hspu]}))

# Get deadlifts @ 225 from Diane
dianeTime = input('What is your Diane Time?\n'
                  '21-15-9\n'
                  'Deadlifts @ 225#\n'
                  'Handstand Pushups\n')
diane_seconds = get_seconds(dianeTime)
alpha_deadlifts = (diane_seconds - 45 * alpha_hspu) / 45.0
alpha_df = alpha_df.append(pd.DataFrame({'movement': 'deadlifts', 'alpha': [alpha_deadlifts]}))


print('hi')
file = open('Data/alpha_library.csv','w')
file.truncate()
file.close()
file = open('Data/alpha_library.csv','a')
for i in range(0, alpha_df.shape[0]):
    file.write('{}, {}\n'.format(alpha_df['movement'].iloc[i], alpha_df['alpha'].iloc[i]))
file.close()