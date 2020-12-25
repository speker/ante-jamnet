# -*- coding: utf-8 -*-
from flask_restful import Resource, Api


class GetTemp(Resource):

    @staticmethod
    def get():
        return {'hello': 'world'}
