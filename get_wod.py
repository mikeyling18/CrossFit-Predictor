from workout_types import WodFormat
import re
import pandas as pd
from string import digits
import alpha_library


def get_wod_components():
    wod_complete_str = ""

    while True:
        wod_component = input("Enter WOD element (Example: 15 pushups)\n")

        if wod_component.lower() == 'done':
            return wod_complete_str
        else:
            reps = int(re.search('[0-9]+', wod_component).group())
            movement = re.sub("\d+|\s+", "", wod_component)

            if 'run' in movement:
                movement = wod_component.lstrip(digits)
                movement = re.sub("\s+", "", movement)
            if 'snatch' in movement:
                movement_with_weight = wod_component.lstrip(digits)
                movement_with_weight = movement_with_weight.replace(" ","")

            movement = movement.lower()
            temp = alpha_library.alpha_df['movement']

            if temp.str.contains(movement).any():
                if 'snatch' in movement:
                    movement = movement_with_weight
                wod_complete_str = wod_complete_str + str(reps) + ' ' + movement + '|'
            else:
                print("No such movement as: ", movement, "please re-enter WOD Component\n")


def add_wod_to_memory(new_wod):
    """

    :param new_wod: boolean
        this is used to determine whether or not the current WOD being processed already exists or not in the history
        .csv file. NOT IMPLEMENTED YET
    :return: List[wod_format, wod_df, time_limit] for AMRAPs
             List[wod_format, wod_df, rounds] for RoundsForTime
    """
    done_entering_wods = False

    while done_entering_wods is not True:
        # Print accepted WOD Formats
        print('Only AMRAPs and RoundsForTime work right now...\n')
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

        if wod_format == WodFormat.AMRAP:
            time_limit = input("What's the time limit? (in mm:ss format)\n")
            wod = get_wod_components()
            if new_wod:
                score = 0
                return [wod_format, pd.DataFrame({'format': [wod_format.name], 'time_limit': [time_limit], 'score': [score],
                                     'WOD': [wod]}), time_limit]
            else:
                score = int(input("Total Reps Complete?\n"))

        # elif wod_format == WodFormat.ForTime:
        #     wod = get_wod_components()
        #     score = input("Time?\n")

        elif wod_format == WodFormat.RoundsForTime:
            rounds = input("How Many Rounds?\n")
            print('Rounds: ', rounds)
            wod = get_wod_components()
            if new_wod:
                score = 0
                return [wod_format, pd.DataFrame({'format': [wod_format.name], 'score': [score], 'WOD': [wod]}), rounds]
            score = input("Time?\n")

        # if new_wod:
        #     return pd.DataFrame({'format': [wod_format.name], 'time_limit': [time_limit], 'score': [score], 'WOD': [wod]}), time_limit
        else:
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
