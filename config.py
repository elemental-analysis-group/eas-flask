import os.path
basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://master:master@localhost/eas'
SQLALCHEMY_TRACK_MODIFICATIONS = True
SECRET_KEY = '123'
FILES='/tmp/eas'
