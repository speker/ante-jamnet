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
        update = cur.execute("UPDATE users SET token=%s where username=%s and user_id=%s", (token,username,user_id ))
        return update
