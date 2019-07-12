from app.models import db, User, Function

#db.drop_all()

for f in Function.query.all():
    print(f)
    db.session.delete(f)

for u in User.query.all():
    print(u)
    db.session.delete(u)

db.session.commit()

