from flask import request

from config import config

conf = globals()
conf.update(config)

from main import app

from disk_usage import disk_usage
from helpers import is_logged_in, write_log
from secrets import secrets

'''
Runtime Config
'''

app.debug = DEBUG

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_PAYLOAD * 1024 * 1024
app.secret_key = secrets['key']

# Commented out to allow somoe.moe and phantom.reticent.io to
# point to Phantom.

# app.config['SERVER_NAME'] = PRODUCTION_URL if not DEBUG else DEV_URL + ':' + str(DEV_PORT)

'''
Inject Template variables
'''

@app.context_processor
def variables():
	total, used, free = disk_usage('/')

	FREE_SPACE = free / (1024 ** 3)

	host = request.url_root\
				.replace('http://', '')\
				.replace('www.', '')\
				.split('/')[0]

	NAME = 'SoMoe' if host == 'somoe.moe' else 'Phantom'
	HEADER = 'SoMoe' if host == 'somoe.moe' else 'Phantom'
	TITLE = None

	if request.endpoint == 'index':
		TITLE = 'SoMoe' if host == 'somoe.moe' else 'Phantom'

	return {
		'NAME': NAME,
		'TITLE': TITLE,
		'HEADER': HEADER,
		'MAX_PAYLOAD': MAX_PAYLOAD,
		'UPLOAD_WAIT': UPLOAD_WAIT,
		'CONTACT': 'phantom@reticent.io',
		'MIN_FREE_DISK': MIN_FREE_DISK,
		'FREE_SPACE': FREE_SPACE,
		'__LOG_ACCESS': write_log('Accessed Page')
	}