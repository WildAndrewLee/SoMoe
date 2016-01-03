from flask import request
from flask.ext.login import current_user

from config import config

conf = globals()
conf.update(config)

from main import app, login_manager
from secrets import secrets
from models.user import User

login_manager.refresh_view = 'login'

login_manager.init_app(app)

@login_manager.user_loader
def load_user(userid):
	return User.getById(int(userid))

'''
Runtime Config
'''

app.debug = DEBUG

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = secrets.cookie_key

'''
Inject Template variables
'''

@app.context_processor
def variables():
	FREE_SPACE = free / (1024 ** 3)

	host = request.url_root\
				.replace('http://', '').replace('https://', '')\
				.replace('www.', '')\
				.split('/')[0]

	NAME = 'SoMoe' if host == 'somoe.moe' else 'Phantom'
	HEADER = 'SoMoe' if host == 'somoe.moe' else 'Phantom'
	TITLE = None
	STYLE = 'moe.css' if host == 'somoe.moe' else 'phantom.css'

	if current_user.is_authenticated():
		max_payload = current_user.max_payload()
	else:
		max_payload = MAX_PAYLOAD

	if request.endpoint == 'index':
		TITLE = 'SoMoe' if host == 'somoe.moe' else 'Phantom'

	return {
		'STYLE': STYLE,
		'NAME': NAME,
		'TITLE': TITLE,
		'HEADER': HEADER,
		'MAX_PAYLOAD': max_payload,
		'UPLOAD_WAIT': UPLOAD_WAIT,
		'CONTACT': 'phantom@reticent.io'
	}
