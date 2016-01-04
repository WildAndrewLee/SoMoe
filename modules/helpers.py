import time
from fcntl import lockf, LOCK_EX, LOCK_UN
from flask import request

from config import config

def get_ip():
	if 'X-Forwarded-For' in request.headers:
		return '|'.join(request.headers.getlist('X-Forwarded-For'))

	return request.remote_addr

def write_log(message):
	if config['LOGGING']:
		with open(config.ACCESS_LOG, 'a') as log:
			now = time.strftime('%I:%M%p %Z on %b %d, %Y')
			ip = get_ip()
			name = ''

			if is_logged_in():
				name = str(session['logged_in']) + ' '

			lockf(f, LOCK_EX)
			log.write(name + ip + ' - ' + now + ' ' + message + '\n')
			lockf(f, LOCK_UN)

	return None