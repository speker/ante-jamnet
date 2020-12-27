# -*- coding: utf-8 -*-
import time

import flask_restful as rest
from flask import jsonify
from helper.modules import Modules
from threading import Thread


class Power(rest.Resource):

    def post(self):
        data = rest.request.get_json(silent=True)
        if data is None or data['power'] is None or data['modules'] is None:
            response = jsonify({'data': {'success': False, 'code': 403, 'message': 'bad module name'}})
            response.status_code = 403
            return response
        power = data['power']
        module_state = data['modules']
        try:
            if power == 1:
                Modules().write_module(0, 0, 0, 1)
                for key in module_state:
                    Modules().write_module(key['module'], key['p1'], key['p2'], 1)
            elif power == 0:
                for key in module_state:
                    Modules().write_module(key['module'], key['p1'], key['p2'], 0)
                work = Thread(target=self.wait_closer)
                work.start()
            return {'data': {'success': 'true'}}
        except Exception as e:
            response = jsonify({'data': {'success': False, 'code': 500, 'message': e}})
            response.status_code = 500
            return response

    @staticmethod
    def wait_closer():
        time.sleep(10)
        Modules().write_module(0, 0, 0, 0)
