#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Administration account configuration for phyapps-gateway service.
"""

from passlib.apps import custom_app_context as pwd_context
from getpass import getpass


admin_name = input("Login name of administrator: ")
admin_pass = getpass("Enter new password: ")
admin_pass_verify = getpass("Verify password: ")

try:
    assert admin_pass == admin_pass_verify
except AssertionError:
    print("Password is not consistent, set failed.")
else:
    phash = pwd_context.encrypt(admin_pass)
    import sys, os
    sys.path.insert(0, os.path.dirname(os.environ['FLASK_APP']))
    from app.models import Admin
    from app.models import db
    admin0 = Admin(nickname=admin_name, password_hash=phash, id=1)
    db.session.add(admin0)
    db.session.commit()

    print("Account '{}' is set.".format(admin_name))
