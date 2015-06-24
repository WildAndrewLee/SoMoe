import time
from flask import request, session
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from config import config
from upload import Upload

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

'''
Used when fetching and serving files.
Updates the last access and returns the sys path.
'''
def get_path(h):
	try:
		path = Upload.query.filter(Upload.h == h).one()
	except NoResultFound, MultipleResultsFound:
		abort(404)

	path.last_updated = time.time()
	path.save()

	path = path.path

	return path