from model.sqlite import SqLite
from helper.gpio import Gpio

last_states = SqLite().get_states()

module_addr = {
    1: {'bridge': 'gpio', 'io': 9, 'state': 1},
    2: {'bridge': 'gpio', 'io': 25, 'state': 1},
    3: {'bridge': 'gpio', 'io': 10, 'state': 1},
    4: {'bridge': 'gpio', 'io': 24, 'state': 1},
    5: {'bridge': 'gpio', 'io': 22, 'state': 1},
    6: {'bridge': 'gpio', 'io': 23, 'state': 1},
    7: {'bridge': 'io_0', 'io': 55, 'state': 1},
    8: {'bridge': 'gpio', 'io': 17, 'state': 1},
    9: {'bridge': 'gpio', 'io': 18, 'state': 1},
    10: {'bridge': 'gpio', 'io': 15, 'state': 1},
    11: {'bridge': 'io_0', 'io': 55, 'state': 1},
    12: {'bridge': 'gpio', 'io': 14, 'state': 1},

}
for key in module_addr:
    bridge = module_addr[key]['bridge']
    io = module_addr[key]['io']
    if bridge == 'gpio':
        module_addr[key]['state'] = Gpio().get_digital(io)
    elif bridge == 'io_0':
        module_addr[key]['state'] = 1
    print(str(key) + ' : ' + str(module_addr[key]['state']))
