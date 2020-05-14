import os
from .default import *


SECRET_KEY = "dev"
DEBUG = True
DB_HOST = 'localhost'
DB_USER = 'grupo18'
DB_PASS = 'ZTI2ZDBiNDUwOGYz'
DB_NAME = 'grupo18'
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root@localhost/grupo18'
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
