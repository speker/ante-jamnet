from model.sqlite import SqLite
from helper.gpio import Gpio

last_states = SqLite().get_states()

module_addr = {
    1: {'bridge': 'gpio', 'io': 9},
    2: {'bridge': 'gpio', 'io': 25},
    3: {'bridge': 'gpio', 'io': 10},
    4: {'bridge': 'gpio', 'io': 24},
    5: {'bridge': 'gpio', 'io': 22},
    6: {'bridge': 'gpio', 'io': 23},
    7: {'bridge': 'gpio', 'io': 0},
    8: {'bridge': 'gpio', 'io': 17},
    9: {'bridge': 'gpio', 'io': 18},
    10: {'bridge': 'gpio', 'io': 15},
    11: {'bridge': 'gpio', 'io': 0},
    12: {'bridge': 'gpio', 'io': 14},

}
for key in module_addr:
    bridge = module_addr[key]['bridge']
    io = module_addr[key]['io']
    if bridge == 'gpio':
        print(str(key)+' : '+str(Gpio().get_digital(io)))
