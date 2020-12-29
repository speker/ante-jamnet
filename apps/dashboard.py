# -*- coding: utf-8 -*-
import flask_restful as rest
from flask import jsonify
import os
import time
from threading import Thread
from subprocess import check_output
from model.sqlite import SqLite


class Dashboard(rest.Resource):
    module_template = '<div class="col-md-3"><div class="card card-|module_state|"><div class="card-header"><h3 class="card-title">Modül : |module_id| - |module_name|</h3><div class="card-tools"><button type="button" class="btn btn-tool" id="clear_alarm_|module_id|"><i class="fas fa-volume-off"></i></button></div></div><div class="card-body" style="display: block;"><span><strong>Power</strong></span><div class="progress mb-3"><div class="progress-bar bg-|module_progress|" role="progressbar" style="width: |module_state|%"></div></div><div class="btn-group btn-group-toggle"  data-toggle="buttons"><label class="btn btn-|module_high|"><input type="radio" name="options" id="module_high_|module_id|" > High</label><label class="btn btn-|module_middle|"><input type="radio" name="options" id="module_middle_|module_id|" > Middle</label><label class="btn btn-|module_low|"><input type="radio" name="options" id="module_low_|module_id|"> Low</label><label class="btn btn-|module_off| "><input type="radio" name="options" id="module_off_|module_id|">|module_power_state|</label></div></div></div></div>'

    def get(self):
        modules = SqLite().get_states()
        module_data = []
        for key in modules:
            module_id = key[0]
            module_p1 = key[1]
            module_p2 = key[2]
            module_error = key[3]
            module_power = key[4]
            module_name = key[5]
            module_clear = key[6]
            module_calc = str(module_p1) + str(module_p2)

            module_high = "default"
            module_middle = "default"
            module_low = "default"

            if module_calc == "00":
                module_high = "success"
                module_middle = "default"
                module_low = "default"
            elif module_calc == "10":
                module_high = "default"
                module_middle = "warning"
                module_low = "default"
            elif module_calc == "01":
                module_high = "default"
                module_middle = "default"
                module_low = "danger"
            if module_power == 1:
                module_power_state = "Off"
            else:
                module_power_state = "On"
            module_is_active = key[7]
            if module_is_active == 1:
                temp = self.module_template
                temp = temp.replace("|module_id|", str(module_id))
                temp = temp.replace("|module_name|", module_name)
                temp = temp.replace("|module_high|", module_high)
                temp = temp.replace("|module_middle|", module_middle)
                temp = temp.replace("|module_low|", module_low)
                temp = temp.replace("|module_power_state|", module_power_state)
                module_data.append(temp)

        return {'data': {'success': True, 'modules': ''.join(module_data)}}
