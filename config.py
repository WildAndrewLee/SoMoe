from flask.ext.login import current_user

config = {
	'UPLOAD_FOLDER': '/var/phantom/uploads',
	'MAX_PAYLOAD': 20,
	'AUTH_PAYLOAD': 35,
	'UPLOAD_WAIT': 10,
	'PORT': 9001,
	'IO_DELAY': 0.025,
	'LOGGING': False,
	'MIN_FREE_DISK': 5,
	'DEBUG': True,
	'PRODUCTION_URL': 'phantom.reticent.io',
	'DEV_URL': 'localhost',
	'DEV_PORT': 9002
}

messages = {
	'MESSAGES': {
		'empty': 'You must choose a file to upload.',
		'slow-down': 'You must wait {} seconds before uploading another file.'.format(config['UPLOAD_WAIT']),
		'too-big': 'The file you are trying to upload is too big.'
	}
}

config.update(messages)