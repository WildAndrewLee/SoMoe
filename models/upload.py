from sqlalchemy import Column, Integer, String, DateTime
from models.db import Model, session_factory

class Upload(Model):
	__tablename__ = 'uploads'
	id = Column(Integer, primary_key = True)
	ip = Column(String(255))
	path = Column(String(255))

	def save(self):
		with session_factory() as sess:
			sess.merge(self)

	def delete(self):
		with session_factory() as sess:
			sess.delete(self)