import smbus

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
        print('port : ' + port)
        if output == 1:
            self.output |= port
        elif output == 0:
            self.output &= ~port
        print('output : ' + self.output)

        self.bus.write_byte_data(self.address, OUTPUT_REG_0, self.output)
        self.bus.write_byte_data(self.address, OUTPUT_REG_1, self.output)

    def set_all_clear(self):
        self.bus.write_byte_data(self.address, OUTPUT_REG_0, 0x00)
        self.bus.write_byte_data(self.address, OUTPUT_REG_1, 0x00)
        self.output = 0x00

    def set_gpio(self, output):
        self.bus.write_byte_data(self.address, OUTPUT_REG_0, output)
        self.bus.write_byte_data(self.address, OUTPUT_REG_1, output)
