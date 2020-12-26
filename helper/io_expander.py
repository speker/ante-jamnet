import smbus

output_registers = {
    1: {'port': 1, 'conf': 0x02},
    2: {'port': 2, 'conf': 0x02},
    3: {'port': 4, 'conf': 0x02},
    4: {'port': 8, 'conf': 0x02},
    5: {'port': 16, 'conf': 0x02},
    6: {'port': 32, 'conf': 0x02},
    7: {'port': 64, 'conf': 0x02},
    8: {'port': 128, 'conf': 0x02},
    9: {'port': 128, 'conf': 0x03},
    10: {'port': 128, 'conf': 0x03},
    11: {'port': 128, 'conf': 0x03},
    12: {'port': 128, 'conf': 0x03},
    13: {'port': 128, 'conf': 0x03},
    14: {'port': 128, 'conf': 0x03},
    15: {'port': 128, 'conf': 0x03},
    16: {'port': 128, 'conf': 0x03},
}

IO0_OUTPUT = 0x00
IO0_INPUT = 0x01
IO1_OUTPUT = 0x00
IO1_INPUT = 0x02
IO2_OUTPUT = 0x00
IO2_INPUT = 0x04
IO3_OUTPUT = 0x00
IO3_INPUT = 0x08
IO4_OUTPUT = 0x00
IO4_INPUT = 0x10
IO5_OUTPUT = 0x00
IO5_INPUT = 0x20
IO6_OUTPUT = 0x00
IO6_INPUT = 0x40
IO7_OUTPUT = 0x00
IO7_INPUT = 0x80

CONFIGURATION_REG_0 = 0x06
CONFIGURATION_REG_1 = 0x07
OUTPUT_REG_0 = 0x02
OUTPUT_REG_1 = 0x03


class IoExpander:
    def __init__(self, address):
        self.bus = smbus.SMBus(1)
        self.address = address
        self.output = 0x00
        self.configuration()

    def configuration(self):
        conf = IO0_OUTPUT | IO1_OUTPUT | IO2_OUTPUT | IO3_OUTPUT | IO4_OUTPUT | IO5_OUTPUT | IO6_OUTPUT | IO7_OUTPUT
        self.bus.write_byte_data(self.address, CONFIGURATION_REG_0, conf)
        self.bus.write_byte_data(self.address, CONFIGURATION_REG_1, conf)

    def set_digital(self, port, output):
        pin = output_registers[port]['port']
        reg = output_registers[port]['conf']
        print('port : ' + str(port))
        if output == 1:
            self.output |= pin
        elif output == 0:
            self.output &= ~pin
        print('output : ' + str(self.output))

        self.bus.write_byte_data(self.address, reg, self.output)

    def set_all_clear(self):
        self.bus.write_byte_data(self.address, OUTPUT_REG_0, 0x00)
        self.bus.write_byte_data(self.address, OUTPUT_REG_1, 0x00)
        self.output = 0x00

    def set_gpio(self, output):
        self.bus.write_byte_data(self.address, OUTPUT_REG_0, output)
        self.bus.write_byte_data(self.address, OUTPUT_REG_1, output)

    def get_register(self, port):
        return port
