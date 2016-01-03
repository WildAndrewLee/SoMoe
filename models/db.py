from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from contextlib import contextmanager
from modules.secrets import secrets

'''
Database Connection via SQLAlchemy
'''
eng = 'mysql://{0}:{1}@reticent.io:3306/{2}'.format(secrets.db.username, secrets.db.password, secrets.db.name)
engine = create_engine(
	eng, pool_recycle=1800
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