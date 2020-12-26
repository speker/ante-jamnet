# -*- coding: utf-8 -*-
import flask_restful as rest
from flask import jsonify
from helper.modules import Modules


class SetModule(rest.Resource):
    io_0 = None
    io_1 = None

    def post(self):
        data = rest.request.get_json(silent=True)
        if data is None or data['module'] is None:
            response = jsonify({'data': {'success': False, 'code': 403, 'message': 'bad module name'}})
            response.status_code = 403
            return response
        module_addr = data['module']
        p1 = data['p1']
        p2 = data['p2']
        power = data['power']
        Modules().write_module(module_addr, p1, p2, power)
        return {'data': {'success': 'true'}, 'payload': {'temp': 's'}}
