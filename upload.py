from sqlalchemy import Column, Integer, String, DateTime
from models import Model, session

'''
Uploads Database Model
'''
class Upload(Model):
	__tablename__ = 'uploads'
	id = Column(Integer, primary_key = True)
	h = Column(String(255))
	ip = Column(String(255))
	path = Column(String(255))
	last_update = Column(DateTime())

	def __init__(self, h, ip, path, last_update):
		self.h = h
		self.ip = ip
		self.path = path
		self.last_update = last_update

	def save(self):
		with session() as sess:
			sess.merge(self)

	def delete(self):
		with session() as sess:
			sess.delete(self)