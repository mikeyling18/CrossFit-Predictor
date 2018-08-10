
import alpha_library

def get_seconds(time_str):
    m,s = time_str.split(':')
    return int(m) * 60 + int(s)

def get_run_times(run_time):
    alpha_800 = 2*(run_time/4.0 - 5)
    alpha_400 = alpha_800/2.0 - 5
    alpha_200 = (alpha_400-20)/2.0
    alpha_100 = (alpha_200-30)/2.0

    run_dict = {
        '800m run' : alpha_800,
        '400m run' : alpha_400,
        '200m run' : alpha_200,
        '100m run' : alpha_100
    }
    run_list = list(run_dict.keys())
    file = open('Data/alpha_library.csv', 'a')
    for i in range(0, len(run_dict)):
        file.write('{}, {}\n'.format(run_list[i], run_dict[run_list[i]]))

benchmarks = ['Mile Time', '2k Row', 'Karen (150 Wall Ball For Time', 'Grace (30 C&Js @ 135)',
              'Isabel (30 Snatches @ 135)', '200 Double Unders For Time', '50 Cal Row For Time']
benchmark_names = ['mile', '2krow', 'karen', 'grace', 'isabel', '200du', '50calrow']
alpha_names = ['1600m_run', '2000m_row', 'wall_ball', 'clean_and_jerk', 'snatch', 'double_under', 'cal_row']

benchmarks_dict = {}

for i in range(0, len(benchmarks)):
    score = input('What was your ' + benchmarks[i] + 'score? (use mm:ss format)\n')
    benchmarks_dict[benchmark_names[i]] = score
    seconds = get_seconds(score)
    alpha_library.alpha_library[str(alpha_names[i])] = seconds / alpha_library.benchmark_rep_dict[alpha_names[i]]

get_run_times(503)

alpha_library_entry_names = list(alpha_library.alpha_library.keys())
file = open('Data/alpha_library.csv','a')
# file.write('movement, alpha\n')
for i in range(0,len(alpha_library.alpha_library)):
    file.write('{}, {}\n'.format(alpha_library_entry_names[i], alpha_library.alpha_library[alpha_library_entry_names[i]]))
