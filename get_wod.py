from workout_types import WodFormat
from Get_Wod_Components import get_wod_components
import movements
import re
import csv

done_entering_wods = False

while(done_entering_wods != True):
    # Print accepted WOD Formats
    for formats in WodFormat:
        print(re.sub(r'.*[.]', '', str(formats)))

    wod_not_found = True

    while wod_not_found:
        wod_format = input("What's the format of the WOD?\n")
        wod_format = re.sub("\s+", "", wod_format)
        if wod_format.lower() in WodFormat.__members__:
            wod_format = WodFormat[wod_format]
            wod_not_found = False
            print('Wod Format Chosen: ', wod_format.name)
        else:
            print('WOD Format not found. Try again\n')


    wod = list()
    wod_tuple = list()




    if wod_format == WodFormat.AMRAP:
        time_limit = input("What's the time limit? (in minutes)\n")
        wod = get_wod_components()
        score = int(input("Total Reps Complete?\n"))

        # create final WOD tuple before writing to CSV file
        wod_tuple = [wod_format.value, time_limit, score, wod]

    elif wod_format == WodFormat.ForTime:
        wod = get_wod_components()
        score = input("Time?\n")
        wod_tuple = [wod_format.value, score, wod]

    elif wod_format == WodFormat.RoundsForTime:
        rounds = input("How Many Rounds?\n")
        print('Rounds: ', rounds)

        wod = get_wod_components()
        score = input("Time?\n")
        wod_tuple = [wod_format.value, rounds, score, wod]


    # Ask User if the Wod is ready to be stored in CSV file
    submit = input("Submit WOD into Memory (y/n)? \n")
    if submit.lower() == 'y':
        if wod_format == WodFormat.AMRAP:
            file = open('Data/amrap_wod_memory.csv', 'a')
            file.write('{}, {}, {}, {}\n'.format(wod_format.name, time_limit, score, wod))

        elif wod_format == WodFormat.RoundsForTime:
            file = open('Data/roundsfortime_wod_memory.csv', 'a')
            file.write('{}, {}, {}, {}\n'.format(wod_format.name, rounds, score, wod))

        elif wod_format == WodFormat.ForTime:
            file = open('Data/fortime_wod_memory.csv', 'a')
            file.write('{}, {}, {}\n'.format(wod_format.name, score, wod))
    else:
        print('bye')

    add_another_wod = input("Would you like to enter another wod (y/n)?\n")
    if add_another_wod.lower() == 'y':
        done_entering_wods = False
    else:
        done_entering_wods = True
