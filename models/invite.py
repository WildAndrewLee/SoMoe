import traceback
from sqlalchemy import Column, Integer, String
from models.db import Model, session_factory

class Invite(Model):
	__tablename__ = 'invites'
	id = Column(Integer, primary_key = True)
	h = Column(String(255))
	name = Column(String(255))

	def __init__(self, h, name):
		self.h = h
		self.name = name

	@staticmethod
	def confirm_invite(name, h):
		with session_factory() as sess:
			try:
				invite = sess.query(Invite).filter(
					Invite.name == name,
					Invite.h == h
				).one()

				sess.expunge(invite)

				return invite
			except:
				return None

	@staticmethod
	def delete_invite(name, h):
		with session_factory() as sess:
			invite = sess.query(Invite).filter(
				Invite.name == name,
				Invite.h == h
			).delete()

	def save(self):
		with session_factory() as sess:
			sess.merge(self)

	def delete(self):
		with session_factory() as sess:
			sess.delete(self)