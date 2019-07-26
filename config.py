# -*- coding: utf-8 -*-

import os

DEBUG = True

db_name = os.environ.get('DB_NAME', 'phyapps_cloud')
db_user = os.environ.get('DB_USER', 'devuser')
db_pass = os.environ.get('DB_PASS', '4e043a583')

basedir = os.path.abspath(os.path.dirname(__file__))

# SQLite
# SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')

# MySQL
SQLALCHEMY_DATABASE_URI = \
   'mysql+pymysql://{db_user}:{db_pass}@{host}/{db_name}'.format(
       db_user=db_user,
       db_pass=db_pass,
       db_name=db_name,
       host='localhost:3307')

SQLALCHEMY_TRACK_MODIFICATIONS = False
