# -*- coding: utf-8 -*-

import re
from datetime import datetime
from flask import url_for

from passlib.apps import custom_app_context as pwd_context

from . import db
from .utils import utc2local
from .utils import get_container
from .utils import get_container_status
from .utils import get_container_name
from .utils import get_container_image
from .utils import get_container_ports
from .utils import get_container_ctime
from .utils import get_container_uptime
from .utils import get_container_shortid
from .utils import get_container_url
from .utils import get_container_mach
from .utils import validate_container


class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    users = db.relationship('User', backref='admin', lazy='dynamic')
    timestamp = db.Column(db.DateTime,
                          default=datetime.utcnow,
                          onupdate=datetime.utcnow)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)
        except NameError:
            return str(self.id)

    @property
    def local_time(self):
        return utc2local(self.timestamp)

    def __repr__(self):
        return "<User '{}'>".format(self.nickname)

    def hash_password(self, passwd):
        self.password_hash = pwd_context.encrypt(passwd)

    def verify_password(self, passwd):
        return pwd_context.verify(passwd, self.password_hash)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    timestamp = db.Column(db.DateTime,
                          default=datetime.utcnow,
                          onupdate=datetime.utcnow)
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))
    description = db.Column(db.String(100))

    password_hash = db.Column(db.String(128))
    containers = db.relationship('Container', backref='user', lazy='dynamic')

    @property
    def local_time(self):
        return utc2local(self.timestamp)

    @property
    def container_name(self):
        try:
            return self.containers[-1].name
        except IndexError:
            return "Unknown"

    @property
    def container_id(self):
        try:
            return self.containers[-1].shortid
        except IndexError:
            return "Unknown"

    @property
    def container_status(self):
        try:
            return self.containers[-1].status
        except IndexError:
            return "Unknown"

    @property
    def notebook_url(self):
        return url_for('proxy_nb', name=self.name)

    def __repr__(self):
        return "<User '{}'>".format(self.name)

    def hash_password(self, pw):
        self.password_hash = pwd_context.encrypt(pw)

    def verify_password(self, passwd):
        return pwd_context.verify(passwd, self.password_hash)

    #
    @property
    def is_authenticated(self):
        return True


class Container(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cid = db.Column(db.String(128), index=True, unique=True)
    # last update ts
    timestamp = db.Column(db.DateTime,
                          default=datetime.utcnow,
                          onupdate=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


    def __repr__(self):
        return "<Container '{}'>".format(self.name)

    @property
    def name(self):
        return get_container_name(self.cid)

    @property
    def shortid(self):
        return get_container_shortid(self.cid)

    @property
    def status(self):
        return get_container_status(self.cid)

    @property
    def image(self):
        return get_container_image(self.cid).tags[0]

    @property
    def ports(self):
        return get_container_ports(self.cid)

    @property
    def ctime(self):
        return get_container_ctime(self.cid)

    @property
    def uptime(self):
        return get_container_uptime(self.cid)

    @property
    def local_time(self):
        return utc2local(self.timestamp)

    @property
    def notebook_url(self):
        return get_container_url(self.cid, 8888)

    @property
    def mach(self):
        return get_container_mach(self.cid)

    def get_container(self):
        return get_container(self.cid)
