# -*- coding: utf-8 -*-
import flask_restful as rest
from model.postgre import PostGre
import datetime


class Logs(rest.Resource):

    def get(self):
        logs = PostGre().get_user_log()
        all_log = []
        for log in logs:
            system_name = str(log[1])
            username = str(log[2])
            user_ip = str(log[3])
            log_date = str(log[4])
            log_action = str(log[5])
            action_detail = str(log[6])
            system_ip = str(log[7])
            logger = '<tr><td>' + system_name + '</td><td>' + username + '</td><td>' + user_ip + '</td><td>' + log_date + '</td><td>' + log_action + '</td><td>' + action_detail + '</td><td>' + system_ip + '</td></tr>'
            all_log.append(logger)

        return {'data': {'success': True, 'payload': ''.join(all_log)}}


