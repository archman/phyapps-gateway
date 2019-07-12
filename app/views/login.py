# -*- coding: utf-8 -*-

from flask import render_template
from flask import Response
from flask import request
from flask import session
from flask import abort
from flask_restful import Resource
from flask_restful import marshal

from ..models import User
from ..models import Admin
from ..models import db
from .user import user_fields
from ..utils import request_json


class UserLoginAPI(Resource):
    def __init__(self):
        super(UserLoginAPI, self).__init__()

    def get(self):
        return Response(
                render_template('login.html',),
                mimetype="text/html")

    def put(self):
        # change login status
        if 'logged_in_admin' in session and session['logged_in_admin']:
            session['logged_in_admin'] = None
        else:
            session['logged_in'] = False
            session['logged_in_user'] = None
        return {'logout': True}, 200

    def post(self):
        # just do login authentication
        # signup --> users/post
        form_input = request.get_json()

        username = form_input.get('username')
        password = form_input.get('password')

        if username is None or password is None:
            abort(400)

        as_admin = form_input.get('check_admin');
        op = form_input.get('op')
        if op == 'login':
            if as_admin:
                user = Admin.query.filter(Admin.nickname==username).first()
            else:
                user = User.query.filter(User.name==username).first()

            if user is None:
                abort(404)

            if user.verify_password(password):
                if as_admin:
                    session['logged_in_admin'] = user.nickname
                    return {'logged_in_admin': user.nickname}, 200
                else:
                    session['logged_in'] = True
                    session['logged_in_user'] = user.name
                    return {'logged_in_user': user.name}, 200
            else:
                abort(401)
        elif op == 'signup':

            #if User.query.filter(User.name==username).first() is not None:
            #    abort(400)

            # register new user
            #user = User(name=username)
            #user.hash_password(password)
            #db.session.add(user)
            #db.session.commit()
            #session['logged_in'] = True
            #session['logged_in_user'] = username
            return {'User account': user.name}, 201
