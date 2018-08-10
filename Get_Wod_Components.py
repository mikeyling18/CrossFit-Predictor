import re
import movements
from string import digits

def get_wod_components():
    wod_component = ""
    wod_complete_str = ""
    reps = int
    wod_complete = list()
    while True:
        wod_component = input("Enter WOD element (Example: 15 pushups)\n")

        if wod_component.lower() == 'done':
            # wod_complete_str = wod_complete_str + wod_component.lower() + '|'
            return wod_complete_str
        else:
            reps = int(re.search('[0-9]', wod_component).group())
            movement = re.sub("\d+|\s+", "", wod_component)
            if 'run' in movement:
                movement = wod_component.lstrip(digits)
                movement = re.sub("\s+", "", movement)
            movement = movement.lower()
            in_dict = movement in movements.movement_dict
            if in_dict is False:
                print("No such movement as: ", movement, "please re-enter WOD Component\n")
            else:
                # wod_complete_str = wod_complete_str + wod_component.lower() + '|'
                wod_complete_str = wod_complete_str + str(reps) + ' ' + movement + '|'
    # return wod_complete_str
