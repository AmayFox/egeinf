from web import db
from web.api.models.user import User

db.drop_all()
db.create_all()

user2 = User('Александр', 'alex', '1718c24b10aeb8099e3fc44960ab6949ab76a267352459f203ea1036bec382c2',
             'SECRET', 'user', 11)
user2.save()


db.session.commit()
