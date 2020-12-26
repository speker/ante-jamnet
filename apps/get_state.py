# -*- coding: utf-8 -*-
from flask import jsonify
import flask_restful as rest
from model.sqlite import SqLite


class GetState(rest.Resource):

    @staticmethod
    def get():
        data = rest.request.get_json(silent=True)
        if data is None or data['module'] is None:
            response = jsonify({'data': {'success': False, 'code': 403, 'message': 'bad module name'}})
            response.status_code = 403
            return response
        module_state = SqLite().get_state(data['module'])
        return {'data': {'success': 'true', 'payload': {'state': module_state}}}
