from model.sqlite import SqLite
from helper.gpio import Gpio
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


def check_error():
    for key in module_addr:
        bridge = module_addr[key]['bridge']
        io = module_addr[key]['io']
        if bridge is not None:
            if bridge == 'gpio':
                module_addr[key]['state'] = 1 - Gpio().get_digital(io)
            SqLite().set_error(key, module_addr[key]['state'])
            print(str(key) + ' : ' + str(module_addr[key]['state']))


if __name__ == "__main__":
    while True:
        check_error()
        time.sleep(1)
