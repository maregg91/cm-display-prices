from gevent import monkey
monkey.patch_all()

import os
from gevent.pywsgi import WSGIServer
from flask_webpage import app

http_server = WSGIServer(('0.0.0.0', 6061), app)
http_server.serve_forever()
