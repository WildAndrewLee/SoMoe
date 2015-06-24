from flask import Flask

from config import config

conf = globals()
conf.update(config)

app = Flask(__name__)

import setup
from routes import *

if __name__ == '__main__':
	app.run(host ='0.0.0.0', port=PORT if not DEBUG else DEV_PORT, threaded=not DEBUG)