# -*- coding: utf-8 -*-
import flask_restful as rest
from flask import jsonify, request
from helper.modules import Modules
from model.sqlite import SqLite
import time
from helper.logger import Logger


class SetModule(rest.Resource):

    @staticmethod
    def post():
        Logger().set_request(request, 'set_module')
        data = rest.request.get_json(silent=True)
        if data is None or data['module'] is None:
            response = jsonify({'data': {'success': False, 'code': 403, 'message': 'bad module name'}})
            response.status_code = 403
            return response
        module_addr = data['module']
        p1 = data['p1']
        p2 = data['p2']
        power = data['power']
        try:
            if module_addr == 0:
                all_module = SqLite().get_states()
                for module in all_module:
                    if module[7] == 1:
                        Modules().write_module(module[0], module[1], module[2], power)
                return {'data': {'success': True}}

            Modules().write_module(module_addr, p1, p2, power)
            if power == 1:
                Modules().write_module(0, 0, 0, 1)
            else:
                all_module = SqLite().get_states()
                all_calc = 0
                for module in all_module:
                    if module[7] == 1 and module[0] != 0:
                        all_calc += module[4]
                if all_calc == 0:
                    Modules().write_module(0, 0, 0, 0)
            return {'data': {'success': True}}
        except Exception as e:
            response = jsonify({'data': {'success': False, 'code': 500, 'message': e}})
            response.status_code = 500
            return response

    @staticmethod
    def wait_closer():
        SqLite().set_state(0, 0, 0, 0)
        time.sleep(60)
        power_state = SqLite().get_state(0)[4]
        if power_state == 0:
            Modules().write_module(0, 0, 0, 0)
