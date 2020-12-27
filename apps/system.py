# -*- coding: utf-8 -*-
import flask_restful as rest
from flask import jsonify
import os
import time
from threading import Thread


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
            return {'data': {'success': 'true'}}

    @staticmethod
    def reboot():
        time.sleep(5)
        os.system('sudo shutdown -r now')
