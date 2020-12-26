from helper.io_expander import IoExpander

import time

io = IoExpander()
for i in range(8):
    io.set_digital(i, 1)
    i += 1
    time.sleep(1)

io.set_all_clear()
