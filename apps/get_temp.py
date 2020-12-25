# -*- coding: utf-8 -*-
from flask_restful import Resource, Api
import glob
import time


class GetTemp(Resource):
    try:
        base_dir = '/sys/bus/w1/devices/'
        device_folder = glob.glob(base_dir + '28*')[0]
        device_file = device_folder + '/w1_slave'
    except Exception as e:
        print(e)
        base_dir = '/sys/bus/w1/devices/'
        device_folder = ""
        device_file = device_folder + '/w1_slave'

    def get(self):
        return {'data': {'success': 'true'}, 'payload': {'temp': str(self.read_temp)}}

    def read_temp_raw(self):
        f = open(self.device_file, 'r')
        lines = f.readlines()
        f.close()
        return lines

    def read_temp(self):
        lines = self.read_temp_raw()
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            lines = self.read_temp_raw()
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos + 2:]
            temp_c = float(temp_string) / 1000.0
            return temp_c
