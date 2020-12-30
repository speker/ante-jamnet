# -*- coding: utf-8 -*-
import flask_restful as rest
from flask import jsonify,request
from model.sqlite import SqLite
from helper.logger import Logger

class ClearError(rest.Resource):

    @staticmethod
    def post():
        Logger().set_request(request,'clear_error')
        data = rest.request.get_json(silent=True)
        if data is None or data['module'] is None:
            response = jsonify({'data': {'success': False, 'code': 403, 'message': 'bad module name'}})
            response.status_code = 403
            return response
        module_addr = data['module']
        try:
            SqLite().set_error_clear(module_addr)
            return {'data': {'success': True}}
        except Exception as e:
            response = jsonify({'data': {'success': False, 'code': 500, 'message': e}})
            response.status_code = 500
            return response
