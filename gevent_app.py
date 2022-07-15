from gevent import monkey
monkey.patch_all()

import os
from gevent.pywsgi import WSGIServer
from flask_webpage import app

# Start a gevent server on port 6061 with the flask app as content.
http_server = WSGIServer(('0.0.0.0', 6061), app)
http_server.serve_forever()
