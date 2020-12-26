import sqlite3
import os


class Database:
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

    def get_register(self, port):
        query = self.db.cursor().execute("SELECT * FROM registers where port=" + port)
        register = query.fetchone()
        return register

    def set_register(self, port, value):
        self.db.cursor().execute("UPDATE registers SET value=" + value + " where port=" + port)
        self.db.commit()
