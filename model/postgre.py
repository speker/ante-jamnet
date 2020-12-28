import psycopg2


class PostGre:
    db = None

    def __init__(self):
        if self.db is None:
            self.db = psycopg2.connect(database="jamnet",
                                       user="reactor",
                                       password="ReActor2019!!..",
                                       host="176.53.10.162",
                                       port="5432")
            self.db.autocommit = True

    def check_user(self, username, password):
        cur = self.db.cursor()
        cur.execute("SELECT * from users where username=%s and password=%s", (username, password))
        rows = cur.fetchall()
        return rows

    def set_user_token(self, user_id, username, token):
        cur = self.db.cursor()
        update = cur.execute("UPDATE users SET token=%s where username=%s and user_id=%s", (token, username, user_id))
        return update

    def set_beat(self, module_name, module_serial, module_ip, module_last_beat, module_temp, module_alarm):
        cur = self.db.cursor()
        cur.execute("SELECT * from network where module_serial=%s", (module_serial,))
        rows = cur.fetchone()
        if rows is None:
            insert = cur.execute(
                "INSERT INTO network (module_name,module_ip,module_serial,module_last_beat,module_temp,module_alarm) VALUES (%s,%s,%s,%s,%s,%s)",
                (module_name, module_ip, module_serial, module_last_beat, module_temp, module_alarm
                 ))
        else:
            update = cur.execute(
                "UPDATE network SET module_name=%s, module_ip=%s, module_last_beat=%s, module_temp=%s, module_alarm=%s where module_serial=%s",
                (module_name, module_ip, module_last_beat, module_temp, module_alarm, module_serial,))


    def get_network(self):
        cur = self.db.cursor()
        cur.execute("SELECT * from network order by module_name asc ")
        rows = cur.fetchall()
        return rows