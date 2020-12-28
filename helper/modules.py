from helper.io_expander import IoExpander
from helper.gpio import Gpio
from model.sqlite import SqLite


class Modules:
    io_0 = None
    io_1 = None
    gpio = None

    module_addr = {
        15: {
            'power': {'bridge': 'io_0', 'io': 15},
            'p1': {'bridge': None, 'io': None},
            'p2': {'bridge': None, 'io': None}
        },
        0: {
            'power': {'bridge': 'io_0', 'io': 16},
            'p1': {'bridge': None, 'io': None},
            'p2': {'bridge': None, 'io': None}
        },
        1: {
            'power': {'bridge': 'gpio', 'io': 6},
            'p1': {'bridge': 'io_0', 'io': 1},
            'p2': {'bridge': 'io_0', 'io': 2}
        },
        2: {
            'power': {'bridge': 'gpio', 'io': 12},
            'p1': {'bridge': 'io_0', 'io': 3},
            'p2': {'bridge': 'io_0', 'io': 4}
        },
        3: {
            'power': {'bridge': 'gpio', 'io': 5},
            'p1': {'bridge': 'io_0', 'io': 5},
            'p2': {'bridge': 'io_0', 'io': 6}
        },
        4: {
            'power': {'bridge': 'gpio', 'io': 7},
            'p1': {'bridge': 'io_0', 'io': 7},
            'p2': {'bridge': 'io_0', 'io': 8}
        },
        5: {
            'power': {'bridge': 'gpio', 'io': 8},
            'p1': {'bridge': 'io_0', 'io': 9},
            'p2': {'bridge': 'io_0', 'io': 10}
        },
        6: {
            'power': {'bridge': 'gpio', 'io': 11},
            'p1': {'bridge': 'io_0', 'io': 11},
            'p2': {'bridge': 'io_0', 'io': 12}
        },
        # 7: {
        #     'power': {'bridge': 'gpio', 'io': 21},
        #     'p1': {'bridge': 'io_1', 'io': 14},
        #     'p2': {'bridge': 'io_1', 'io': 13}
        # },
        7: {
            'power': {'bridge': 'gpio', 'io': 16},
            'p1': {'bridge': 'io_1', 'io': 12},
            'p2': {'bridge': 'io_1', 'io': 11}
        },
        8: {
            'power': {'bridge': 'gpio', 'io': 20},
            'p1': {'bridge': 'io_1', 'io': 10},
            'p2': {'bridge': 'io_1', 'io': 9}
        },
        9: {
            'power': {'bridge': 'gpio', 'io': 26},
            'p1': {'bridge': 'io_1', 'io': 8},
            'p2': {'bridge': 'io_1', 'io': 7}
        },
        # 11: {
        #     'power': {'bridge': 'gpio', 'io': 13},
        #     'p1': {'bridge': 'io_1', 'io': 6},
        #     'p2': {'bridge': 'io_1', 'io': 5}
        # },
        10: {
            'power': {'bridge': 'gpio', 'io': 19},
            'p1': {'bridge': 'io_1', 'io': 4},
            'p2': {'bridge': 'io_1', 'io': 3}
        }
    }

    def __init__(self):
        try:
            self.io_0 = IoExpander(0X20)
            self.io_1 = IoExpander(0X21)
            self.gpio = Gpio()
        except Exception as e:
            print(e)

    @staticmethod
    def read_gpio(port):
        return Gpio().get_digital(port)

    def write_module(self, module_addr, p1, p2, power):
        modules = []
        if module_addr == 'clear_all':
            self.io_0.set_all_clear()
            self.io_1.set_all_clear()
            return None
        elif module_addr == "all":
            for i in range(11):
                modules.append(i)
        else:
            modules.append(module_addr)

        for modules in modules:
            power_bridge = self.module_addr[modules]['power']['bridge']
            power_io = self.module_addr[modules]['power']['io']
            p1_bridge = self.module_addr[modules]['p1']['bridge']
            p1_io = self.module_addr[modules]['p1']['io']
            p2_bridge = self.module_addr[modules]['p2']['bridge']
            p2_io = self.module_addr[modules]['p2']['io']

            if power_bridge is not None:
                bridge = getattr(self, power_bridge)
                bridge.set_digital(power_io, power)
            if p1_bridge is not None:
                bridge = getattr(self, p1_bridge)
                bridge.set_digital(p1_io, p1)
            if p2_bridge is not None:
                bridge = getattr(self, p2_bridge)
                bridge.set_digital(p2_io, p2)
            SqLite().set_state(modules, p1, p2, power)
