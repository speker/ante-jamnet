# -*- coding: utf-8 -*-
import flask_restful as rest
from flask import jsonify
import os
import time
from threading import Thread
from subprocess import check_output
from model.sqlite import SqLite


class System(rest.Resource):
    module_template = '<div class="col-md-3"><div class="card card-success"><div class="card-header"><h3 class="card-title">Modül - |module_id|</h3></div><div class="card-body"><div class="form-group"><label for="module_name-|module_id|">Modül Adı</label><input type="text" class="form-control" id="module_name-|module_id|" value="|module_name|" placeholder="Modül Adı"></div><div class="form-check"><input type="checkbox" class="form-check-input" id="is_active-|module_id|" |is_active|><label class="form-check-label" for="is_active-|module_id|" >Aktif</label></div></div><div class="card-footer"><button type="button" id="save-|module_id|" class="btn btn-success">Kaydet</button></div></div></div>'

    def post(self):
        data = rest.request.get_json(silent=True)
        if data is None or data['action'] is None:
            response = jsonify({'data': {'success': False, 'code': 403, 'message': 'bad module name'}})
            response.status_code = 403
            return response
        action = data['action']
        if action == "restart":
            work = Thread(target=self.reboot)
            work.start()
            return {'data': {'success': True}}
        elif action == "shutdown":
            work = Thread(target=self.shutdown)
            work.start()
            return {'data': {'success': True}}
        elif action == "hostname":
            data = os.system('hostnamectl set-hostname ' + data['hostname'])
            return {'data': {'success': True, "message": "Sistem Adı Değiştirildi"}}

    def get(self):
        modules = SqLite().get_states()
        module_data = []
        for key in modules:
            module_id = key[0]
            module_name = key[5]
            module_is_active = key[7]
            if module_is_active == 1:
                is_active = "checked"
            else:
                is_active = ""
            temp = self.module_template
            temp = temp.replace("|module_id|", str(module_id))
            temp = temp.replace("|module_name|", module_name)
            temp = temp.replace("|is_active|", is_active)
            module_data.append(temp)

        return {'data': {'success': True, 'hostname': check_output(['hostname']).decode("utf-8").strip(),
                         "modules": ''.join(module_data)}}

    @staticmethod
    def reboot():
        time.sleep(5)
        os.system('sudo shutdown -r now')

    @staticmethod
    def shutdown():
        time.sleep(5)
        os.system('sudo shutdown -h now')
