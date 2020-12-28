# -*- coding: utf-8 -*-
import flask_restful as rest
from model.postgre import PostGre
import datetime


class Network(rest.Resource):
    template = '<div class="col-sm-3 col-6"><div class="small-box bg-|net_state|"><div class="inner"><h4><strong>' \
               '|module_ip|</strong></h4><span><strong>|module_name|</strong> <br>|module_serial|<br>Sıcaklık : ' \
               '<strong>|module_temp|&deg;</strong><br>Güncelleme : <strong>|module_last_beat|</strong></span>' \
               '</div><div class="icon"><i class="ion ion-stats-bars"></i></div>' \
               '<a href="http://|module_ip|/dashboard.html" class="small-box-footer">' \
               'Dashboard <i class="fas fa-arrow-circle-right"></i></a></div></div>'

    def get(self):
        network = PostGre().get_network()
        if network is not None:
            net_data = []
            for key in network:
                module_name = key[1]
                module_ip = key[2]
                module_serial = key[3]
                module_last_beat = str(key[4])[0:19]
                module_temp = str(key[5])[0:4]
                module_alarm = key[6]
                offline_dif = key[4] + datetime.timedelta(0, 300)
                now = datetime.datetime.now()
                if offline_dif < now:
                    net_state = "danger"
                else:
                    if module_alarm is False:
                        net_state = "success"
                    else:
                        net_state = "warning"
                temp = self.template
                temp = temp.replace("|module_name|", module_name)
                temp = temp.replace("|module_ip|", module_ip)
                temp = temp.replace("|module_serial|", module_serial)
                temp = temp.replace("|module_last_beat|", module_last_beat)
                temp = temp.replace("|module_temp|", module_temp)
                temp = temp.replace("|net_state|", net_state)
                net_data.append(temp)
            return {'data': {'success': True, 'payload': ''.join(net_data)}}
