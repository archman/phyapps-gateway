# -*- coding: utf-8 -*-

from flask import abort
from flask import render_template
from flask import Response
from flask import session

from flask_restful import Resource
from flask_restful import fields
from flask_restful import marshal
from flask_restful import reqparse

from ..models import User
from ..models import Admin
from ..models import Container
from ..models import db
from ..auth import auth
from ..utils import request_json
from ..utils import validate_container
from ..fields import user_fields
from ..proxy import update_proxy


class UserAPI(Resource):
    #decorators = [auth.login_required]
    def __init__(self):
        self.rp = reqparse.RequestParser()
        self.rp.add_argument('name', type=str, location='json')
        self.rp.add_argument('password', type=str, location='json')
        self.rp.add_argument('description', type=str, location='json')
        self.rp.add_argument('container_name', type=str, location='json')
        self.rp.add_argument('server_url', type=str, location='json')
        super(UserAPI, self).__init__()

    def get(self, name):
        user = User.query.filter(User.name==name).first()

        if user is None:
            abort(404)

        if request_json():
            return {'user': marshal(user, user_fields)}
        return Response(
                    render_template('show_user.html',
                        user=marshal(user, user_fields),
                        title="Inspection of {}".format(name)),
                    mimetype='text/html')

    #@auth.login_required
    def put(self, name):
        # update user configuration.
        # name, password, description
        # todo: handle admin?
        user = User.query.filter(User.name==name).first()
        if user is None:
            abort(404)
        args = self.rp.parse_args()
        for k, v in args.items():
            if k == 'container_name':
                self._update_container(user, v)
            elif k == 'password' and v not in [None, '']:
                user.hash_password(v)
            elif v is not None:
                setattr(user, k, v)

        db.session.commit()
        return {'user': marshal(user, user_fields)}

    def _update_container(self, user, cname):
        """Update container for user.
        """
        cid, c = validate_container(cname)
        new_c = Container.query.filter_by(cid=cid).first()
        if c is not None:
            try:
                self._clean_containers(user.containers[:-1])
                #for idx, ic in enumerate(user.containers[:-1]):
                #    try:
                #        print('removing', ic)
                #        db.session.delete(ic)
                #        ic.get_container().stop()
                #        ic.get_container().remove()
                #    except:
                #        print(ic)
                #db.session.commit()
            except:
                print("stop container")
            # start container
            user.containers[-1].get_container().start()
            # update proxy rule
            update_proxy(user.name, new_c.notebook_url)
            print('update with new container')

    def _clean_containers(self, cobj):
        # cobj: list of container model object
        for idx, ic in enumerate(cobj):
            try:
                db.session.delete(ic)
                ic.get_container().stop()
                ic.get_container().remove()
            except:
                print("Clean Error")
        db.session.commit()


    #@auth.login_required
    def delete(self, name):
        user = User.query.filter(User.name==name).first()
        if user is None:
            abort(404)
        # delete container
        self._clean_containers(user.containers)
        # delete user
        db.session.delete(user)
        db.session.commit()
        return {'result': True}


class UserListAPI(Resource):
    #decorators = [auth.login_required]
    def __init__(self):
        self.rp = reqparse.RequestParser()
        self.rp.add_argument('username', type=str, required=True,
                help='No username provided', location='json')
        self.rp.add_argument('password', type=str, required=True,
                help='No password provided', location='json')
        self.rp.add_argument('description', type=str, default='TBA',
                location='json')
        super(UserListAPI, self).__init__()

    def get(self):
        users = User.query.all()
        if request_json():
            return {'users': [marshal(u, user_fields) for u in users]}
        return Response(
                    render_template('show_users.html',
                        users=[marshal(u, user_fields) for u in users]),
                        mimetype='text/html')

    def put(self):
        # fix urls
        all_users = User.query.all()
        for u in all_users:
            nb_url0 = u.containers[-1].notebook_url
            if nb_url0 != 'Unknown':
                update_proxy(u.name, nb_url0)
            # update URL (API) --> (URL (PROXY)) in Containers/admin panel
        return {'resule': True}, 200

    #@auth.login_required
    def post(self):
        user = self.rp.parse_args()

        username = user.get('username')
        password = user.get('password')

        if username is None or username == '':
            return {'error': 'Invalid username'}, 400
        if password is None or password == '':
            return {'error': 'Invalid password'}, 400

        u = User.query.filter(User.name==username).first()
        if u is not None:
            return {'error': 'user exists'}, 400
        else:
            if 'logged_in_admin' in session:
                admin_name = session['logged_in_admin']
                admin = Admin.query.filter_by(nickname=admin_name).first()
            else:
                admin = Admin.query.filter_by(id=1).first()

            new_u = User(name=username,
                         admin=admin,
                         description=user.get('description'),
                    )
            new_u.hash_password(user.get('password'))
            db.session.add(new_u)
            db.session.commit()
            session['logged_in_user'] = username
            session['logged_in'] = True
            return {'user': marshal(new_u, user_fields)}, 201
