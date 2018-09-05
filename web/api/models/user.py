from web import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256))
    login = db.Column(db.String(256))
    password = db.Column(db.String(1024))
    code = db.Column(db.String(256))
    role = db.Column(db.String(256))
    grade = db.Column(db.Integer)
    photo = db.Column(db.String(256))

    def __init__(self, name, login, password, code, role, grade=0, photo='0'):
        self.name = name
        self.login = login
        self.password = password
        self.code = code
        self.role = role
        self.grade = grade
        self.photo = photo

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self.id

    @staticmethod
    def get_all():
        return User.query.all()

    @staticmethod
    def get_all_one_grade(grade):
        return db.session.query(User).filter(User.grade == grade).all()

    @staticmethod
    def update_by_login(login, key, value):
        db.session.query(User).filter(User.login == login).update({key: value}, synchronize_session='evaluate')
        db.session.commit()
