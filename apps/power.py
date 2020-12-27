# -*- coding: utf-8 -*-
import flask_restful as rest
from flask import jsonify
from helper.modules import Modules
from model.sqlite import SqLite


class Power(rest.Resource):

    @staticmethod
    def post():
        data = rest.request.get_json(silent=True)
        if data is None or data['power'] is None:
            response = jsonify({'data': {'success': False, 'code': 403, 'message': 'bad module name'}})
            response.status_code = 403
            return response
        power = data['power']
        remove_item = [13, 11, 7, 0]
        module_state = SqLite().get_states()
        for item in remove_item:
            del module_state[item]
        try:
            if power == 1:
                for key in module_state:
                    Modules().write_module(key[0], key[1], key[2], key[3]-1)
            elif power == 0:
                for key in module_state:
                    Modules().write_module(key[0], key[1], key[2], key[3]-1)
            return {'data': {'success': 'true'}}
        except Exception as e:
            response = jsonify({'data': {'success': False, 'code': 500, 'message': e}})
            response.status_code = 500
            return response
