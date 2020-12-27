# -*- coding: utf-8 -*-
import flask_restful as rest
from flask import jsonify


class Login(rest.Resource):

    def post(self):
        data = rest.request.get_json(silent=True)
        if data is None:
            response = jsonify({'data': {'success': False, 'code': 403, 'message': 'bad module name'}})
            response.status_code = 403
            return response
        username = data['username']
        password = data['password']
        print(username)
