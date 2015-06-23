from functools import wraps
# why...
from flask import request, Response, session, flash

from helpers import write_log, is_logged_in

'''
Authentication

THIS WAS STOLEN FROM THE FLASK TUTORIAL SITE BECAUSE
I WAS TOO LAZY TO DO ACTUAL AUTH.

LEGIT AUTH WILL BE PUT IN SO I CAN ACTUALLY DELETE
FILES VIA URL INSTEAD OF NEEDING TO SSH IN EVERY TIME.

This is also ugly so please don't use this--please.

'''

def check_auth(username, password):
	"""This function is called to check if a username /
	password combination is valid.
	"""
	admins = [
	]

	users = [
	]

	users = users.extend(admins)

	try:
		try:
			return next(x for x in users if x[0] == username and x[1] == password)
		finally:
			session['admin'] = True

		return next(x for x in users if x[0] == username and x[1] == password)
	except:
		return False
	finally:
		if not 'admin' in session:
			session['admin'] = False

def authenticate():
	"""Sends a 401 response that enables basic auth"""
	return Response(
	'Could not verify your access level for that URL.\n'
	'You have to login with proper credentials', 401,
	{'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
	@wraps(f)
	def decorated(*args, **kwargs):
		auth = request.authorization

		if not auth or (not is_logged_in() and not check_auth(auth.username, auth.password)):
			return authenticate()

		if not session['logged_in']:
			session['logged_in'] = auth.username
			flash('You have logged in as {}. To logout, close your browser--really.'.format(auth.username))

		return f(*args, **kwargs)
	return decorated
