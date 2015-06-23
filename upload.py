from models import db

'''
Uploads Database Model
'''
class Upload(db.Model):
	__tablename__ = 'uploads'
	id = db.Column(db.Integer, primary_key = True)
	h = db.Column(db.String(255))
	ip = db.Column(db.String(255))
	path = db.Column(db.String(255))
	last_update = db.Column(db.DateTime())

	def __init__(self, h, ip, path, last_update):
		self.h = h
		self.ip = ip
		self.path = path
		self.last_update = last_update

	def save(self):
		db.session.merge(self)
		db.session.commit()

	def delete(self):
		db.session.delete(self)
		db.session.commit()