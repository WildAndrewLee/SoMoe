from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from secrets import db

'''
Database Connection via SQLAlchemy
'''
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://{0}:{1}@reticent.io:3306/{2}'.format(db['username'], db['password'], db['name'])
db = SQLAlchemy(app)