from flask import Flask
from flask.ext.login import LoginManager

app = Flask(__name__)
login_manager = LoginManager()

import setup
from routes import *

if __name__ == '__main__':
	app.run(host ='0.0.0.0', port=PORT if not DEBUG else DEV_PORT, threaded=not DEBUG)