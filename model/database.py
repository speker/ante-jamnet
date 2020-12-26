import sqlite3
import os


class Database:
    db = None

    def __init__(self):
        if self.db is None:
            script_path = os.path.dirname(os.path.abspath(__file__))
            connection = sqlite3.connect(script_path + '/jamnet.db', detect_types=sqlite3.PARSE_COLNAMES)
            self.db = connection.cursor()

    def get_states(self):
        query = self.db.execute("SELECT * FROM module_states")
        states = query.fetchall()
        return states

    def get_state(self, module):
        query = self.db.execute("SELECT * FROM module_states where module_addr=" + str(module))
        states = query.fetchone()
        return states
