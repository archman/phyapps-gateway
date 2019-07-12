# -*- coding: utf-8 -*-

from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

import os

template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            '../templates')
static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          '../static')

app = Flask(__name__,
            template_folder=template_dir,
            static_folder=static_dir)
app.config.from_object('config')
app.secret_key = os.urandom(20)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

api = Api(app)

from .views import UserAPI
from .views import UserListAPI
from .views import ContainerAdminAPI
from .views import UserAdminAPI
from .views import UserLoginAPI

from flask import Response
from flask import render_template


@app.route('/')
def index():
    return Response(
            render_template('index.html', title="Phyapps Cloud"),
            mimetype="text/html")


@app.route('/<string:name>/', methods=['GET'])
def proxy_nb(name):
    return Response(
            render_template('nb_404.html'),
            mimetype="text/html")


api.add_resource(UserAPI, '/users/<string:name>',
                 endpoint='user')
api.add_resource(UserListAPI, '/users',
                 endpoint='users')
api.add_resource(ContainerAdminAPI, '/containers/<string:name>',
                 endpoint='container')
api.add_resource(UserAdminAPI, '/users/admin',
                 endpoint='u_admin')
api.add_resource(UserLoginAPI, '/users/login',
                 endpoint='u_login')
#api.add_resource(ProxyAPI, '/<string:name>',
#                 endpoint='user_nb')

# session:
# logged_in [bool]
# logged_in_user [string], logged_in_admin [string]
