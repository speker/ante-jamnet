from model.postgre import PostGre
from datetime import datetime
from jwt import (
    JWT,
    jwk_from_pem
)
from subprocess import check_output
import json


class Logger:
    with open('/opt/ante-jamnet/helper/certs/rsa_private_key.pem', 'rb') as fh:
        signing_key = jwk_from_pem(fh.read())

    def set_request(self, request, action=None):
        log_date = datetime.now()
        user_ip = request.remote_addr
        action_detail = request.json
        instance = JWT()
        username = None
        if 'token' in action_detail:
            token = action_detail['token']
            decode = instance.decode(token, self.signing_key)
            username = decode['user_name']
            del action_detail['token']

        if 'action' in action_detail:
            action = action_detail['action']

        module_ip = check_output(['hostname', '--all-ip-addresses']).decode("utf-8").strip()
        system_name = check_output(['hostname']).decode("utf-8").strip()
        PostGre().set_user_log(self.get_serial(), system_name, username, user_ip, log_date, action,
                          json.dumps(action_detail), module_ip)

    @staticmethod
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


    def set_alarm(self,module_name,action):
        print()
