# -*- coding: utf-8 -*-
import flask_restful as rest
from flask import jsonify, request
import os
import time
from threading import Thread
from subprocess import check_output
from model.sqlite import SqLite
from helper.logger import Logger


class System(rest.Resource):
    module_template = '<div class="col-md-3"><div class="card card-success"><div class="card-header"><h3 class="card-title">Modül - |module_id|</h3></div><div class="card-body"><div class="form-group"><label for="module_name_|module_id|">Modül Adı</label><input type="text" class="form-control" id="module_name_|module_id|" value="|module_name|" placeholder="Modül Adı"></div><div class="form-check"><input type="checkbox" class="form-check-input" id="is_active_|module_id|" |is_active|><label class="form-check-label" for="is_active_|module_id|" >Aktif</label></div></div><div class="card-footer"><button type="button" id="save_|module_id|" class="btn btn-success">Kaydet</button></div></div></div>'

    def post(self):
        Logger().set_request(request)
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

        elif action == "save_module":
            module_id = data['module_id']
            module_name = data['module_name']
            is_active = data['is_active']
            SqLite().update_state(module_id, module_name, is_active)
            return {'data': {'success': True, "message": "Modül Bilgileri Güncellendi"}}

        elif action == "set_pg_db":
            pg_ip = data['pg_ip']
            pg_port = data['pg_port']
            pg_username = data['pg_username']
            pg_password = data['pg_password']

            SqLite().set_system_value('pg_ip', pg_ip)
            SqLite().set_system_value('pg_port', pg_port)
            SqLite().set_system_value('pg_username', pg_username)
            SqLite().set_system_value('pg_password', pg_password)
            return {'data': {'success': True, "message": "Veritabanı Bilgileri Güncellendi"}}
        elif action == "set_ip":
            if 'eth_ip' in data and 'eth_gateway' in data:
                eth_ip=data['eth_ip']
                eth_gateway=data['eth_gateway']
                ip_temp="interface eth0 \n" \
                        "static ip_address=|eth_ip|\n" \
                        "static routers=|eth_gateway|\n" \
                        "static domain_name_servers=8.8.8.8\n" \
                        "\n" \
                        "interface wlan0\n" \
                        "static ip_address=192.168.88.240/24\n" \
                        "static routers=192.168.88.1\n" \
                        "static domain_name_servers=8.8.8.8"
                ip_temp = ip_temp.replace("|eth_ip|", str(eth_ip))
                ip_temp = ip_temp.replace("|eth_gateway|", str(eth_gateway))

                f = open("/etc/dhcpcd.conf", "w")
                f.write(ip_temp)
                f.close()
                return {'data': {'success': True, "message": "Ip Adresi Güncellendi"}}

            else :
                response = jsonify({'data': {'success': False, 'code': 403, 'message': 'Hatalı Adres Bilgisi'}})
                response.status_code = 403



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
            pg_ip = SqLite().get_system_value('pg_ip')
            pg_port = SqLite().get_system_value('pg_port')
            pg_username = SqLite().get_system_value('pg_username')
            pg_password = SqLite().get_system_value('pg_password')
            return {'data': {'success': True, 'hostname': check_output(['hostname']).decode("utf-8").strip(),
                             'modules': ''.join(module_data),
                             'pg_db': {'pg_ip': pg_ip, 'pg_port': pg_port, 'pg_username': pg_username,
                                       'pg_password': pg_password}}}

    @staticmethod
    def reboot():
        time.sleep(5)
        # os.system('sudo shutdown -r now')

    @staticmethod
    def shutdown():
        time.sleep(5)
        os.system('sudo shutdown -h now')
