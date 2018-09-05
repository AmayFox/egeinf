from web import db
from flask_login import UserMixin


class Answer(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(256))
    correct = db.Column(db.Boolean)
    task_id = db.Column(db.Integer)

    def __init__(self, content, correct, task_id):
        self.content = content
        self.correct = correct
        self.task_id = task_id

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self.id

    @staticmethod
    def get_all():
        return Answer.query.all()

    @staticmethod
    def get_all_answers_from_task(task_id):
        return db.session.query(Answer).filter(Answer.task_id == task_id).all()

    @staticmethod
    def update_by_id(id, key, value):
        db.session.query(Answer).filter(Answer.id == id).update({key: value}, synchronize_session='evaluate')
        db.session.commit()
