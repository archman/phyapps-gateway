# -*- coding: utf-8 -*-

from flask_restful import fields


container_fields = {
    'name': fields.String,
    'longid': fields.String(attribute='cid'),
    'shortid': fields.String(attribute='shortid'),
    'status': fields.String,
    'image': fields.String,
    'ctime': fields.String,
    'uptime': fields.String,
    'ports': fields.String,
    'timestamp': fields.String(attribute='local_time'),
    'owner': fields.String(attribute=lambda x:x.user.name),
    'notebook_url': fields.String(attribute='notebook_url'),
    'mach': fields.String(attribute='mach')
}


admin_fields = {
    'nickname': fields.String,
    'email': fields.String,
    'timestamp': fields.String(attribute='local_time'),
}


user_fields = {
    'name': fields.String,
    'uri': fields.Url('user', absolute=False),
    'description': fields.String,
    'notebook_url': fields.String(attribute='notebook_url'),
    'container_name': fields.String(attribute='container_name'),
    'container_id': fields.String(attribute='container_id'),
    'container_status': fields.String(attribute='container_status'),
    'timestamp': fields.String(attribute='local_time'),
    'password_hash': fields.String,
    'creator': fields.String(attribute=lambda x:x.admin.nickname),
}

