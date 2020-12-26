from helper.io_expander import IoExpander

import time

io_0 = IoExpander(0X20)
io_1 = IoExpander(0X21)
for i in range(8):
    io_0.set_digital(i, 1)
    io_1.set_digital(i, 1)
    i += 1
    time.sleep(1)

# io_0.set_all_clear()
# io_1.set_all_clear()
