from model.sqlite import SqLite
from helper.modules import Modules
import time

module_addr = {
    1: {'bridge': 'gpio', 'io': 9, 'state': 0},
    2: {'bridge': 'gpio', 'io': 25, 'state': 0},
    3: {'bridge': 'gpio', 'io': 10, 'state': 0},
    4: {'bridge': 'gpio', 'io': 24, 'state': 0},
    5: {'bridge': 'gpio', 'io': 22, 'state': 0},
    6: {'bridge': 'gpio', 'io': 23, 'state': 0},
    7: {'bridge': None, 'io': None, 'state': 0},
    8: {'bridge': 'gpio', 'io': 17, 'state': 0},
    9: {'bridge': 'gpio', 'io': 18, 'state': 0},
    10: {'bridge': 'gpio', 'io': 15, 'state': 0},
    11: {'bridge': None, 'io': None, 'state': 0},
    12: {'bridge': 'gpio', 'io': 14, 'state': 0},

}


def get_error():
    for key in module_addr:
        bridge = module_addr[key]['bridge']
        io = module_addr[key]['io']
        if bridge is not None:
            if bridge == 'gpio':
                module_addr[key]['state'] = 1 - Modules().read_gpio(io)
            SqLite().set_error(key, module_addr[key]['state'])


def set_alarm(state):
    # Modules().write_module(15, 0, 0, state)
    Modules().write_module("led", 0, 0, state)


def check_error():
    modules = SqLite().get_errors()
    alarm = 0
    for key in modules:
        module = key[0]
        error = key[1]
        clear = key[2]
        if error == 1 and clear == 0:
            alarm = 1
    return alarm


if __name__ == "__main__":
    alarm_state = 0
    while True:
        get_error()
        if check_error() == 1 and alarm_state == 0:
            alarm_state = 1
            set_alarm(alarm_state)
        if check_error() == 0 and alarm_state == 1:
            alarm_state = 0
            set_alarm(alarm_state)
        time.sleep(1)
