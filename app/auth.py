from flask_httpauth import HTTPBasicAuth
from flask import make_response
from flask import jsonify
from flask import session
from flask import Response
from flask import render_template

from passlib.apps import custom_app_context

from .models import User
from .models import Admin
from .utils import request_json

auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(username, password):
    # if not found logged in admins, pop up authentication dialog
    if 'logged_in_admin' in session and session['logged_in_admin']:
        return True
    else:
        u = Admin.query.filter(Admin.nickname==username).first()
        if not u:
            return False
        if u.verify_password(password):
            session['logged_in_admin'] = u.nickname
            return True
        return False
    """
    # user or admin
    u = Admin.query.filter(Admin.nickname==username).first()
    if not u:
        return False
    if u.verify_password(password):
        session['logged_in_admin'] = True
        return True
    else:
        session['logged_in_admin'] = False
        return False
    #return u.verify_password(password)
    #return custom_app_context.verify(password, users.get(username))
    """

@auth.error_handler
def unauthorized():
    if request_json():
        return make_response(jsonify({'error': 'Unauthorized access'}), 401)
    return Response(
                render_template('admin_401.html'),mimetype='text/html')
