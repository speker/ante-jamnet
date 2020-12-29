# -*- coding: utf-8 -*-
import flask_restful as rest
from flask import jsonify
import os
import time
from threading import Thread
from subprocess import check_output
from model.sqlite import SqLite


class Dashboard(rest.Resource):
    module_template = '<div class="col-sm-3"><div class="card card-|module_state|"><div class="card-header"><h4 class="card-title">|module_id| - |module_name|</h4><div class="card-tools"><button type="button" class="btn btn-tool" id="clear_alarm_|module_id|"><i class="fas fa-volume-off"></i></button></div></div><div class="card-body" style="display: block;"><span><strong>Power</strong></span><div class="progress mb-3"><div class="progress-bar bg-|module_progress|" role="progressbar" style="width: |module_state_level|%"></div></div><div class="btn-group btn-group-toggle"  data-toggle="buttons"><label class="btn btn-|module_high|"><input type="radio" name="options" id="module_high_|module_id|" > High</label><label class="btn btn-|module_middle|"><input type="radio" name="options" id="module_middle_|module_id|" > Middle</label><label class="btn btn-|module_low|"><input type="radio" name="options" id="module_low_|module_id|"> Low</label><label class="btn btn-|module_off| "><input type="radio" name="options"  value="|module_power|" id="module_off_|module_id|">|module_power_state|</label></div></div></div></div>'
    module_template_0 = '<div class="col-md-3"><div class="card card-|module_state|"><div class="card-header"><h4 class="card-title">Modül : |module_id| - |module_name|</h4></div><div class="card-body" style="display: block;"><button type="button"  class="btn btn-|module_off|" id="module_off_|module_id|" >|module_power_state|</button></div></div></div></div>'

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
            module_is_active = key[7]

            module_calc = str(module_p1) + str(module_p2)

            module_high = "default"
            module_middle = "default"
            module_low = "default"
            temp = None

            if module_calc == "00":
                module_high = "secondary"
                module_middle = "default"
                module_low = "default"
                module_state_level = 100
                module_progress = "success"
            elif module_calc == "10":
                module_high = "default"
                module_middle = "secondary"
                module_low = "default"
                module_state_level = 50
                module_progress = "warning"
            elif module_calc == "01":
                module_high = "default"
                module_middle = "default"
                module_low = "secondary"
                module_state_level = 25
                module_progress = "danger"
            if module_power == 1:
                module_power_state = "Off"
                module_off = "danger"
                if module_error == 1 and module_clear == 0:
                    module_state = "warning"
                elif module_error == 1 and module_clear == 1:
                    module_state = "success"
                else:
                    module_state = "success"
            else:
                module_power_state = "On"
                module_off = "success"
                module_state = "danger"
                module_state_level = 0
            if module_is_active == 1:
                if module_id == 0:
                    temp = self.module_template_0
                else:
                    temp = self.module_template
                temp = self.module_template
                temp = temp.replace("|module_id|", str(module_id))
                temp = temp.replace("|module_name|", module_name)
                temp = temp.replace("|module_high|", module_high)
                temp = temp.replace("|module_middle|", module_middle)
                temp = temp.replace("|module_low|", module_low)
                temp = temp.replace("|module_power_state|", module_power_state)
                temp = temp.replace("|module_off|", module_off)
                temp = temp.replace("|module_state|", module_state)
                temp = temp.replace("|module_state_level|", str(module_state_level))
                temp = temp.replace("|module_progress|", module_progress)
                temp = temp.replace("|module_power|", str(module_power) + module_calc)
                module_data.append(temp)

        return {'data': {'success': True, 'modules': ''.join(module_data)}}
