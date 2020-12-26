# -*- coding: utf-8 -*-
import flask_restful as rest
from flask import jsonify
from helper.modules import Modules


class SetModule(rest.Resource):

    @staticmethod
    def post():
        data = rest.request.get_json(silent=True)
        if data is None or data['module'] is None:
            response = jsonify({'data': {'success': False, 'code': 403, 'message': 'bad module name'}})
            response.status_code = 403
            return response
        module_addr = data['module']
        p1 = data['p1']
        p2 = data['p2']
        power = data['power']
        try:
            Modules().write_module(module_addr, p1, p2, power)
            return {'data': {'success': 'true'}}
        except Exception as e:
            response = jsonify({'data': {'success': False, 'code': 500, 'message': e}})
            response.status_code = 500
            return response
