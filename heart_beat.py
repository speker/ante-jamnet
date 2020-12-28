from model.postgre import PostGre
from model.sqlite import SqLite
import time
from subprocess import check_output
from datetime import datetime
from apps.get_temp import GetTemp


def get_serial():
    cpu_serial = "0000000000000000"
    try:
        f = open('/proc/cpuinfo', 'r')
        for line in f:
            if line[0:6] == 'Serial':
                cpu_serial = line[10:26]
        f.close()
    except:
        cpu_serial = "ERROR000000000"
    return cpu_serial


def send_beat():
    module_last_beat = datetime.now()
    module_ip = check_output(['hostname', '--all-ip-addresses']).decode("utf-8").strip()
    module_name = check_output(['hostname']).decode("utf-8").strip()
    module_serial = get_serial()
    module_temp = str(GetTemp().read_temp())
    module_alarm = SqLite().get_error_state()
    PostGre().set_beat(module_name, module_serial, module_ip, module_last_beat, module_temp, module_alarm)


if __name__ == "__main__":
    while True:
        try:
            send_beat()
        except:
            time.sleep(60)
        time.sleep(10)
