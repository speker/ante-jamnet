# -*- coding: utf-8 -*-
import time

import flask_restful as rest
from flask import jsonify
from helper.modules import Modules
from model.sqlite import SqLite


class Power(rest.Resource):

    @staticmethod
    def post():
        data = rest.request.get_json(silent=True)
        if data is None or data['power'] is None or data['modules'] is None:
            response = jsonify({'data': {'success': False, 'code': 403, 'message': 'bad module name'}})
            response.status_code = 403
            return response
        power = data['power']
        module_state = data['modules']
        try:
            if power == 1:
                Modules().write_module(0, 0,0, 1)
                for key in module_state:
                    Modules().write_module(key[0], key[1], key[2], 1)
            elif power == 0:
                for key in module_state:
                    Modules().write_module(key[0], key[1], key[2], 0)
                time.sleep(1)
                Modules().write_module(key[0], key[1], key[2], 0)
            return {'data': {'success': 'true'}}
        except Exception as e:
            response = jsonify({'data': {'success': False, 'code': 500, 'message': e}})
            response.status_code = 500
            return response
