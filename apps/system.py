# -*- coding: utf-8 -*-
import flask_restful as rest
from flask import jsonify
import os


class System(rest.Resource):

    @staticmethod
    def post():
        data = rest.request.get_json(silent=True)
        if data is None or data['action'] is None:
            response = jsonify({'data': {'success': False, 'code': 403, 'message': 'bad module name'}})
            response.status_code = 403
            return response
        action = data['action']
        if action == "restart":
            os.system('sudo shutdown -r now')

