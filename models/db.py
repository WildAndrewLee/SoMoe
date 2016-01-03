from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from contextlib import contextmanager

from config import config
from modules.secrets import secrets

eng = config.CONNECTION_STRING.format(secrets.db.username, secrets.db.password, secrets.db.name)
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