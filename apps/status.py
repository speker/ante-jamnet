# -*- coding: utf-8 -*-
import flask_restful as rest
from model.database import Database


class Status(rest.Resource):
    modules_states = None

    def __init__(self):
        try:
            self.modules_states = Database().get_states()
        except Exception as e:
            print(e)

    def get(self):
        return {'data': {'success': 'true', 'payload': {'states': self.modules_states}}}
