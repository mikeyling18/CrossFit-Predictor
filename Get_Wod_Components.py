import re
from movements import Movements

def get_wod_components():
    wod_component = ""
    wod_complete_str = ""
    wod_complete = list()
    while wod_component.lower() != 'done':
        wod_component = input("Enter WOD element (Example: 15 pushups)\n")
        movement = re.sub("\d+| \s+", "", wod_component)
        movement = movement.lower()
        if movement in Movements.__members__ is False:
            print("No such movement as: ", movement, "please re-enter WOD Component\n")
        else:
            if wod_component.lower() != 'done':
                wod_complete_str = wod_complete_str + wod_component.lower() + ' | '
    return wod_complete_str
