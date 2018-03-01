import os.path
basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True
#SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir,'app.db')
SQLALCHEMY_DATABASE_URI = 'postgres://eas:eas@localhost:5432/eas'
SQLALCHEMY_TRACK_MODIFICATIONS = True
SECRET_KEY = '123'
