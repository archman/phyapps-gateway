# -*- coding: utf-8 -*-

from flask import abort
from flask import request
from flask import Response
from flask import render_template
from flask_restful import Resource
from flask_restful import fields
from flask_restful import marshal

from ..utils import validate_container
from ..utils import create_new_container
from ..utils import request_json
from ..fields import container_fields
from ..models import Container
from ..models import User
from ..models import db


class ContainerAdminAPI(Resource):
    def __init__(self):
        super(ContainerAdminAPI, self).__init__()

    def get(self, name):
        """
        Parameters
        ----------
        nam : str
            Container name.
        """
        cid, _ = validate_container(name)
        container = Container.query.filter_by(cid=cid).first()
        if not container:
            abort(404)

        if request_json():
            return {'container': marshal(container, container_fields)}
        return Response(
                render_template('show_container.html',
                    container=marshal(container, container_fields)),
                mimetype='text/html')

    def post(self, name):
        # new
        data = request.get_json()
        try:
            u = User.query.filter(User.name==data['uname']).first()
            new_cid, new_cname, new_url1, new_url2 = \
                create_new_container(user=u, **data)
            new_container = Container(cid=new_cid)

            if u is None:
                abort(404)
            new_container.user = u
            db.session.add(new_container)
            db.session.commit()

            return {'id': new_cid, 'name': new_cname, 'nb_url': new_url1, 'ss_url': new_url2}, 201
        except:
            return {'id': None, 'name': 'Unknown', 'nb_url': None, 'ss_url': None}, 501

    def put(self, name):
        # upate
        cid, c = validate_container(name)
        container = Container.query.filter_by(cid=cid).first()
        if not container:
            abort(404)
        op = request.get_json().get('op')
        if op == "stop":
            if c.status == 'running':
                return self._stop(c), 200
        elif op == "pause":
            if c.status == 'running':
                return self._pause(c), 200
        elif op == "start":
            if c.status in ('created', 'exited'):
                return self._start(c), 200
        elif op == "resume":
            if c.status == 'paused':
                return self._resume(c), 200

    def _stop(self, c):
        print("{} has just been stopped.".format(c.id))
        c.stop()
        return {"status": "exited"}

    def _start(self, c):
        print("{} has just been started.".format(c.id))
        c.start()
        return {"status": "running"}

    def _resume(self, c):
        print("{} has just been resumed.".format(c.id))
        c.unpause()
        return {"status": "running"}

    def _pause(self, c):
        print("{} has just been paused.".format(c.id))
        c.pause()
        return {"status": "paused"}
