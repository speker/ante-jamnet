from model.sqlite import SqLite

remove_item = [13, 11, 7, 0]
module_state = SqLite().get_states()
for item in remove_item:
        del module_state[item]
for key in module_state:
    print(key)
