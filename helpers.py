import time
from flask import request, session

from config import config

'''
Helper Functions
'''

def is_logged_in():
	return bool('logged_in' in session and session['logged_in'])

def get_ip():
	if 'X-Forwarded-For' in request.headers:
		return '|'.join(request.headers.getlist('X-Forwarded-For'))

	return request.remote_addr

def write_log(message):
	if config['LOGGING']:
		with open('/var/phantom/access_log', 'a') as log:
			now = time.strftime('%I:%M%p %Z on %b %d, %Y')
			ip = get_ip()
			name = ''

			if is_logged_in():
				name = str(session['logged_in']) + ' '

			log.write(name + ip + ' - ' + now + ' ' + message + '\n')

	return None