from model.database import Database
from helper.modules import Modules
last_states = Database().get_states()
for key in last_states:
    module_addr = key[0]
    p1 = key[1]
    p2 = key[2]
    power = key[4]
    print(module_addr,p1,p2,power)
    try:
        Modules().write_module(module_addr, p1, p2, power)
    except Exception as e:
        print(e)