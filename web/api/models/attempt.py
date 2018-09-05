from web import db
from flask_login import UserMixin


class Attempt(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(256))
    task_id = db.Column(db.Integer)
    status = db.Column(db.String(256))

    def __init__(self, author, task_id, status):
        self.author = author
        self.task_id = task_id
        self.status = status

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self.id

    @staticmethod
    def get_all():
        return Attempt.query.all()

    @staticmethod
    def update_by_id(id, key, value):
        db.session.query(Attempt).filter(Attempt.id == id).update({key: value}, synchronize_session='evaluate')
        db.session.commit()
