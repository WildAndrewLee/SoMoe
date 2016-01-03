import os, sys

sys.dont_write_bytecode = True

from modules.secrets import secrets

os.environ['AWS_ACCESS_KEY_ID'] = secrets.AWS_ACCESS_KEY_ID
os.environ['AWS_SECRET_ACCESS_KEY'] = secrets.AWS_SECRET_ACCESS_KEY

from flask import Flask
from flask.ext.login import LoginManager

app = Flask(__name__)
login_manager = LoginManager()

import modules.setup
from modules.routes import *

if __name__ == '__main__':
	app.run(host ='0.0.0.0', debug=True, port=PORT if not DEBUG else DEV_PORT, threaded=not DEBUG)
