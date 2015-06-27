from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from contextlib import contextmanager
from secrets import db

'''
Database Connection via SQLAlchemy
'''
eng = 'mysql://{0}:{1}@reticent.io:3306/{2}'.format(db['username'], db['password'], db['name'])
engine = create_engine(
	eng
)

factory = sessionmaker(bind=engine)
Session = scoped_session(factory)
Model = declarative_base()

@contextmanager
def session_factory():
	s = Session()

	try:
		yield s
		s.commit()
	except:
		s.rollback()
		raise
	finally:
		s.close()