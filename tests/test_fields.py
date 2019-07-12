import sys
sys.path.insert(0, '../')

from flask_restful import marshal

from app.models import Container
from app.fields import container_fields
from app.fields import user_fields

from app.models import User
from app.models import db

c1 = Container.query.all()[0]
print marshal(c1, container_fields)

#for k,v in marshal(c1, container_fields).items():
#    print(k, v)

#u1 = User.query.all()[0]
#print u1.containers

#for k,v in marshal(u1, user_fields).items():
#    print(k, v)


