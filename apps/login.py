# -*- coding: utf-8 -*-
import flask_restful as rest
from flask import jsonify
from model.postgre import PostGre
from datetime import datetime, timedelta
import jwt


class Login(rest.Resource):

    def post(self):
        data = rest.request.get_json(silent=True)
        if data is None:
            response = jsonify({'data': {'success': False, 'code': 403, 'message': 'bad module name'}})
            response.status_code = 403
            return response
        username = data['username']
        password = data['password']
        user = PostGre().check_user(username, password)
        if len(user) == 0:
            response = jsonify({'data': {'success': False, 'code': 401, 'message': 'Kullanıcı Adı veya Şifre Hatalı'}})
            response.status_code = 401
            return response
        else:
            user_id = user[0][0]
            JWT_SECRET = '7n?P3gjjJqDCbgZrS4QD#hz+a83pLrD3rJwdtWbx-K#%jkYf%B_2n$ha$*bY9CUp'
            JWT_ALGORITHM = 'HS256'
            JWT_EXP_DELTA_SECONDS = 1728000
            payload = {
                'user_name': username,
                'user_id': user_id,
                'exp': datetime.utcnow() + timedelta(seconds=JWT_EXP_DELTA_SECONDS)
            }
            jwt_token = jwt.encode(payload, JWT_SECRET, JWT_ALGORITHM).decode('utf-8')
            PostGre().set_user_token(user_id, username, jwt_token)
            return {'data': {'success': True, 'token': jwt_token}}
