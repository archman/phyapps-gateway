# -*- coding: utf-8 -*-

from flask import render_template
from flask import Response
from flask import request
from flask import abort
from flask_restful import Resource
from flask_restful import marshal
from flask_restful import reqparse

from ..models import Admin
from ..models import User
from ..models import Container
from ..models import db
from ..auth import auth
from ..fields import user_fields
from ..fields import admin_fields
from ..fields import container_fields


class UserAdminAPI(Resource):
    def __init__(self):
        self.rp = reqparse.RequestParser()
        self.rp.add_argument('nickname', type=str, required=True)
        self.rp.add_argument('password', type=str, location='json')
        self.rp.add_argument('email', type=str, location='json', default="not available")
        super(UserAdminAPI, self).__init__()

    @auth.login_required
    def get(self):
        users = User.query.all()
        admins = Admin.query.all()
        containers = Container.query.all()
        #
        #if request_json():
        #    return {'users': [marshal(u, user_fields) for u in users]}
        return Response(
                    render_template('show_admin.html',
                        users=[marshal(u, user_fields) for u in users],
                        containers=[marshal(c, container_fields) for c in containers],
                        admins=[marshal(u, admin_fields) for u in admins]),
                        mimetype='text/html')

    def put(self):
        p = self.rp.parse_args()
        nickname = p.get('nickname')
        password = p.get('password')
        email = p.get('email')

        if nickname in [None, '']:
            abort(400)

        admin = Admin.query.filter(Admin.nickname==nickname).first()

        if password not in [None, '']:
            admin.hash_password(password)
        if email not in [None, '']:
            admin.email = email
        db.session.commit()
        return {'Updated admin account': nickname}, 200

    def post(self):
        admin = self.rp.parse_args()
        nickname = admin.get('nickname')
        password = admin.get('password')
        email = admin.get('email')

        if nickname in [None, ''] or password in [None, '']:
            abort(400)

        if Admin.query.filter(Admin.nickname==nickname).first() is not None:
            abort(400)

        new_admin = Admin(nickname=nickname, email=email)
        new_admin.hash_password(password)
        db.session.add(new_admin)
        db.session.commit()
        return {'Admin account': new_admin.nickname}, 201

    def delete(self):
        p = self.rp.parse_args()
        admin = Admin.query.filter(Admin.nickname==p.get('nickname')).first()
        if admin is None:
            abort(404)
        db.session.delete(admin)
        db.session.commit()
        return {'result': True}

