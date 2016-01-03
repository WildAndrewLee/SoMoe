config = {
	'UPLOAD_FOLDER': '/tmp/',
	'MAX_PAYLOAD': 20,
	'AUTH_PAYLOAD': 35,
	'UPLOAD_WAIT': 10,
	'PORT': 9001,
	'IO_DELAY': 0.025,
	'LOGGING': False,
	'MIN_FREE_DISK': 5,
	'DEBUG': True,
	'DEV_URL': 'localhost',
	'DEV_PORT': 9002,
	'EMAIL': 'andrew@reticent.io',
	'ACCESS_LOG': '/var/phantom/access_log',
	'CONNECTION_STRING': 'mysql://{0}:{1}@reticent.io:3306/{2}',

	'script': {
		'EXIF_TOOL': '/usr/bin/exiftool -q -all= {path}',
		'CLAMDSCAN': '/usr/bin/clamdscan {path} | /usr/bin/clamdscan --remove -',
		# 31104000 = 1 year in seconds
		'UPLOAD_AWS': '/usr/local/bin/aws s3 cp {path} s3://neko.somoe.moe/{rel_path} --cache-control max-age=31104000 && /bin/rm -r {path}'
	}
}

messages = {
	'messages': {
		'EMPTY': 'You must choose a file to upload.',
		'SLOW_DOWN': 'You must wait {} seconds before uploading another file.'.format(config['UPLOAD_WAIT']),
		'TOO_BIG': 'The file you are trying to upload is too big.',
		'VIRUS': 'Your upload could not be completed because it was detected to be a virus.',
		'BAD_INVITE': 'Oops. Looks like somebody gave you a bad invite.'
	}
}

config.update(messages)

from modules.object import Object

config = Object(config)