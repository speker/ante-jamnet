# -*- coding: utf-8 -*-
import flask_restful as rest
from flask import jsonify
from model.postgre import PostGre
from datetime import datetime, timedelta, timezone
from jwt import (
    JWT,
    jwk_from_pem
)
from jwt.utils import get_int_from_datetime


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
            instance = JWT()
            user_id = user[0][0]
            JWT_SECRET = '7n?P3gjjJqDCbgZrS4QD#hz+a83pLrD3rJwdtWbx-K#%jkYf%B_2n$ha$*bY9CUp'
            JWT_ALGORITHM = 'HS256'
            JWT_EXP_DELTA_SECONDS = 1728000
            with open('../helper/certs/rsa_private_key.pem', 'rb') as fh:
                signing_key = jwk_from_pem(fh.read())
            payload = {
                'iss': 'Ante-Jamnet',
                'user_name': username,
                'iat': get_int_from_datetime(datetime.now(timezone.utc)),
                'user_id': user_id,
                'exp': get_int_from_datetime(
                    datetime.now(timezone.utc) + timedelta(hours=240)),
            }
            jwt_token = instance.encode(payload, signing_key, JWT_ALGORITHM).decode('utf-8')
            PostGre().set_user_token(user_id, username, jwt_token)
            return {'data': {'success': True, 'token': jwt_token}}
