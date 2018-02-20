#encoding: utf-8
import os

DEBUG = True
SECRET_KEY = os.urandom(24)

HOSTNAME = '127.0.0.1'
PORT = '3306'
DATABASE = 'forum'
USERNAME = 'forum'
PASSWORD = 'forum'
DB_URI = 'mysql://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME,PASSWORD,HOSTNAME,PORT,DATABASE)
#DB_URI = 'mysql://root:sunnya.527@127.0.0.1/forum'
SQLALCHEMY_DATABASE_URI = DB_URI

