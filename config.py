import os.path
basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True
#SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://master:master@localhost/eas'
SQLALCHEMY_DATABASE_URI = 'sqlite:////home/thiago/_files/eas.db'
SQLALCHEMY_TRACK_MODIFICATIONS = True
SECRET_KEY = '123'
FILES='/home/thiago/_files/'
