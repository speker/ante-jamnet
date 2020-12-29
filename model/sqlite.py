import sqlite3
import os


class SqLite:
    db = None

    def __init__(self):
        if self.db is None:
            script_path = os.path.dirname(os.path.abspath(__file__))
            connection = sqlite3.connect(script_path + '/jamnet.db', detect_types=sqlite3.PARSE_COLNAMES)
            self.db = connection

    def get_states(self):
        query = self.db.cursor().execute("SELECT * FROM module_states")
        states = query.fetchall()
        return states

    def get_state(self, module):
        query = self.db.cursor().execute("SELECT * FROM module_states where module_addr=" + str(module))
        states = query.fetchone()
        return states

    def get_register(self, port, address):
        query = self.db.cursor().execute(
            "SELECT * FROM registers where port=" + str(port) + " and address=" + str(address))
        register = query.fetchone()
        return register[1]

    def set_register(self, port, address, value):
        self.db.cursor().execute(
            "UPDATE registers SET value=" + str(value) + " where port=" + str(port) + " and address=" + str(address))
        self.db.commit()

    def set_state(self, module, p1, p2, power):
        self.db.cursor().execute(
            "UPDATE module_states SET p1=" + str(p1) + ", p2=" + str(p2) + ", power=" + str(
                power) + " where module_addr=" + str(module))
        self.db.commit()

    def set_error_clear(self, module):
        self.db.cursor().execute("UPDATE module_states SET clear_error=1 where module_addr=" + str(module))
        self.db.commit()

    def set_error(self, module, value):
        if value == 0:
            self.db.cursor().execute(
                "UPDATE module_states SET error=" + str(value) + ", clear_error=0 where module_addr=" + str(module))
        else:
            self.db.cursor().execute(
                "UPDATE module_states SET error=" + str(value) + " where module_addr=" + str(module))
        self.db.commit()

    def get_errors(self):
        query = self.db.cursor().execute("SELECT module_addr,error,clear_error FROM module_states")
        states = query.fetchall()
        return states

    def get_error_state(self):
        query = self.db.cursor().execute(
            "SELECT module_addr,error,clear_error FROM module_states where error='1' and clear_error='0' ")
        states = query.fetchone()
        if states is None:
            return False
        else:
            return True

    def update_state(self, module_id, module_name, is_active):
        self.db.cursor().execute(
            "UPDATE module_states SET module_name='" + module_name + "', is_active=" + str(
                is_active) + " where module_addr=" + str(module_id))
        self.db.commit()

    def get_system_value(self, system):
        query = self.db.cursor().execute("SELECT value FROM system where system='" + str(system)+"'")
        value = query.fetchone()
        return value[0]