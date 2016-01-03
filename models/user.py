from functools import wraps
from flask import abort
from sqlalchemy import Column, Integer, String
from flask.ext.login import current_user

from models.db import Model, session_factory
from config import config

def requires_role(role):
	def wrapper(route):
		@wraps(route)
		def r(*args, **kwargs):
			if current_user.is_authenticated() and current_user.role <= role:
				return route(*args, **kwargs)
			else:
				abort(404)
		return r
	return wrapper

'''
User Database Model
'''
class User(Model):
	__tablename__ = 'users'
	id = Column(Integer, primary_key = True)
	role = Column(Integer, default=1)
	username = Column(String)
	h = Column(String)
	max_load = Column(Integer)
	is_auth = None

	# Cache results of auth check because
	# it's expensive to query the DB 5 million
	# times every page load. This way we only do it
	# once.
	def is_authenticated(self):
		if not self.is_auth == None:
			return self.is_auth

		with session_factory() as sess:
			try:
				sess.query(User).filter(
					User.username == self.username,
					User.h == self.h
				).one()

				self.is_auth = True
				return True
			except:
				self.is_auth = False
				return False

	def max_payload(self):
		if self.max_load:
			if self.max_load > config['AUTH_PAYLOAD']:
				return self.max_load
			else:
				return config['AUTH_PAYLOAD']
		else:
			return config['MAX_PAYLOAD']

	# Users are always active.
	def is_active(self):
		return True

	def is_anonymous(self):
		return False

	def get_id(self):
		return unicode(self.id)

	@staticmethod
	def get_by_name(username):
		with session_factory() as sess:
			try:
				user = sess.query(User).filter(
					User.username==username
				).one()

				sess.expunge(user)
				return user
			except:
				return None

	@staticmethod
	def get_by_id(userid):
		with session_factory() as sess:
			try:
				user = sess.query(User).filter(
					User.id == userid
				).one()
				
				sess.expunge(user)

				return user
			except:
				return None

	def save(self):
		with session_factory() as sess:
			sess.merge(self)

	def delete(self):
		with session_factory() as sess:
			sess.delete(self)