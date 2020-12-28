# -*- coding: utf-8 -*-
import flask_restful as rest
from flask import jsonify
import os
import time
from threading import Thread
from subprocess import check_output


class System(rest.Resource):

    def post(self):
        data = rest.request.get_json(silent=True)
        if data is None or data['action'] is None:
            response = jsonify({'data': {'success': False, 'code': 403, 'message': 'bad module name'}})
            response.status_code = 403
            return response
        action = data['action']
        if action == "restart":
            work = Thread(target=self.reboot)
            work.start()
            return {'data': {'success': True}}
        elif action == "shutdown":
            work = Thread(target=self.shutdown)
            work.start()
            return {'data': {'success': True}}
        elif action == "hostname":
            data = os.system('hostnamectl set-hostname ' + data['hostname'])
            return {'data': {'success': True, "message": "Modül Adı Değiştirildi"}}

    @staticmethod
    def get():
        return {'data': {'success': True, 'hostname': check_output(['hostname']).decode("utf-8").strip()}}

    @staticmethod
    def reboot():
        time.sleep(5)
        os.system('sudo shutdown -r now')

    @staticmethod
    def shutdown():
        time.sleep(5)
        os.system('sudo shutdown -h now')
