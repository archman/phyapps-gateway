#!/usr/bin/env python
# -*- coding: utf8 -*-

"""Initialize admin
"""

import sys
sys.path.insert(0, '../')

from app.models import Admin
from app.models import db


_admin0 = {
    'name': 'compadmin',
    'hash': '$6$rounds=656000$3bP2.doJoQbi4JBi$SftaJWRdM8crEFjVcZ2Oa7GmpoHOQsRQuWLPO2JMyaUti8UhuYM9LOO2GSWoLUVpy9prcoleqVY.K.rC8okVG0'
}

admin0 = Admin(nickname=_admin0['name'], password_hash=_admin0['hash'],
               email='admin@localhost', id=1)

# default admin account
db.session.add(admin0)
db.session.commit()
