import os

DEBUG = True
#SERVER_NAME = '127.0.0.1:5050'

basedir = os.path.abspath(os.path.dirname(__file__))

# SQLite
# SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')

# MySQL
SQLALCHEMY_DATABASE_URI = \
   'mysql+pymysql://{username}:{password}@{host}/phyapps_cloud'.format(
       username='devuser',
       password='E=mc^2',
       host='localhost:3307')

SQLALCHEMY_TRACK_MODIFICATIONS = False
