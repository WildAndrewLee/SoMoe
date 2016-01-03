from flask import request
from flask.ext.login import current_user

from config import config
from secrets import secrets
from main import app, login_manager
from models.user import User

login_manager.refresh_view = 'login'

login_manager.init_app(app)

@login_manager.user_loader
def load_user(userid):
	return User.get_by_id(int(userid))

'''
Runtime Config
'''

app.debug = config.DEBUG

app.config['UPLOAD_FOLDER'] = config.UPLOAD_FOLDER
app.secret_key = secrets.cookie_key

'''
Inject Template variables
'''

@app.context_processor
def variables():
	host = request.url_root\
				.replace('http://', '')\
				.replace('https://', '')\
				.replace('www.', '')\
				.split('/')[0]

	if current_user.is_authenticated():
		max_payload = current_user.max_payload()
	else:
		max_payload = config.MAX_PAYLOAD

	return {
		'MAX_PAYLOAD': max_payload,
		'UPLOAD_WAIT': config.UPLOAD_WAIT,
		'CONTACT': config.EMAIL
	}
