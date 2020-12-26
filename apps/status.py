# -*- coding: utf-8 -*-
import flask_restful as rest
from model.sqlite import SqLite


class Status(rest.Resource):
    modules_states = None

    def __init__(self):
        try:
            self.modules_states = SqLite().get_states()
        except Exception as e:
            print(e)

    def get(self):
        return {'data': {'success': 'true', 'payload': {'states': self.modules_states}}}
