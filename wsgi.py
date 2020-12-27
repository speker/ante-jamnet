# -*- coding: utf-8 -*-
from api import app

host = '0.0.0.0'
port = 8000
if __name__ == "__main__":
    app.run(host=host, port=port, debug=True, threaded=True, use_reloader=True)
