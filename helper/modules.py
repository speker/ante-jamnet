from helper.io_expander import IoExpander


class Modules:
    io_0 = None
    io_1 = None

    module_addr = {
        'alarm': {
            'power': {'bridge': 'io_0', 'io': 15},
            'p1': {'bridge': None, 'io': None},
            'p2': {'bridge': None, 'io': None}
        },
        0: {
            'power': {'bridge': 'io_0', 'io': 16},
            'p1': {'bridge': None, 'io': None},
            'p2': {'bridge': None, 'io': None}
        }
    }

    def __init__(self):
        try:
            self.io_0 = IoExpander(0X20)
            self.io_1 = IoExpander(0X21)
        except Exception as e:
            print(e)

    def write_module(self, module_addr, p1, p2, power):
        if module_addr == 'clear_all':
            self.io_0.set_all_clear()
            self.io_1.set_all_clear()
            return None
        power_bridge = self.module_addr[module_addr]['power']['bridge']
        power_io = self.module_addr[module_addr]['power']['io']
        p1_bridge = self.module_addr[module_addr]['p1']['bridge']
        p1_io = self.module_addr[module_addr]['p1']['io']
        p2_bridge = self.module_addr[module_addr]['p2']['bridge']
        p2_io = self.module_addr[module_addr]['p2']['io']

        if power_bridge is not None:
            bridge = getattr(self, power_bridge)
            bridge.set_digital(power_io, power)
        if p1_bridge is not None:
            bridge = getattr(self, p1_bridge)
            bridge.set_digital(p1_io, p1)
        if p2_bridge is not None:
            bridge = getattr(self, p2_bridge)
            bridge.set_digital(p2_io, p2)
