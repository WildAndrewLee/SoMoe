import os, sys

from flask import Flask
from flask.ext.bcrypt import Bcrypt
from flask.ext.login import LoginManager

from config import config
from modules.secrets import secrets
import modules.setup

sys.dont_write_bytecode = True

os.environ['AWS_ACCESS_KEY_ID'] = secrets.AWS_ACCESS_KEY_ID
os.environ['AWS_SECRET_ACCESS_KEY'] = secrets.AWS_SECRET_ACCESS_KEY

app = Flask(__name__)
login_manager = LoginManager()

bcrypt = Bcrypt(app)

from modules.routes import *

if __name__ == '__main__':
	app.run(
		host ='0.0.0.0',
		debug=True,
		port=config.PORT if not config.DEBUG else config.DEV_PORT,
		threaded=not config.DEBUG
	)
