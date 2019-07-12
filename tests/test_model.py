#!/usr/bin/env python

"""test User and Container

Tong Zhang <zhangt@frib.msu.edu>
2017-11-15 16:20:57 PM EST
"""
import sys
sys.path.insert(0, '../')

from app.models import db
from app.models import User
from app.models import Admin
from app.models import Container


admin = Admin(nickname='admin', email='admin@google.com')

user1 = User(name='testuser1')
user1.admin = admin

container = Container(cid="24b015815e76")
container.user = user1

db.session.add(container)
db.session.commit()


