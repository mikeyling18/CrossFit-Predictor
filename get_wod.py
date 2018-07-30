from workout_types import WodFormat
from Get_Wod_Components import get_wod_components
from movements import Movements
import re
import csv


# Print accepted WOD Formats
for formats in WodFormat:
    print(re.sub(r'.*[.]', '', str(formats)))

wod_not_found = True

while wod_not_found:
    wod_format = input("What's the format of the WOD?\n")
    if wod_format in WodFormat.__members__:
        wod_format = WodFormat[wod_format]
        wod_not_found = False
        print('Wod Format Chosen: ', wod_format.name)
    else:
        print('WOD Format not found. Try again\n')


wod = list()
wod_tuple = list()




if wod_format == WodFormat.AMRAP:
    time_limit = input("What's the time limit? (in minutes)\n")
    # print('Time Limit: ', time_limit, 'minutes')

    wod = get_wod_components()
    # print(wod)
    score = int(input("Total Reps Complete?\n"))
    # print('Score: ', score)

    # create final WOD tuple before writing to CSV file
    wod_tuple = [wod_format.value, time_limit, score, wod]
    # print(wod_tuple)


elif wod_format == WodFormat.RoundsForTime:
    rounds = input("How Many Rounds?\n")
    print('Rounds: ', rounds)

    wod = get_wod_components()
    score = input("Time?\n")
    wod_tuple = [wod_format.value, score, wod]


# Ask User if the Wod is ready to be stored in CSV file
submit = input("Submit WOD into Memory (Y/N)? \n")
if submit == 'Y':
    if wod_format == WodFormat.AMRAP:
        file = open('wod_memory.csv', 'a')
        file.write('{}, {} minutes, {} reps, {}\n'.format(wod_format.name, time_limit, score, wod))

    elif wod_format == WodFormat.RoundsForTime:
        file = open('wod_memory.csv', 'a')
        file.write('{}, {}, {}\n'.format(wod_format.name, score, wod))
else:
    print('bye')

