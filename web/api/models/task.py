from web import db
from flask_login import UserMixin


class Task(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(1024))
    tag = db.Column(db.String(256))
    rating = db.Column(db.Integer)
    picture = db.Column(db.String(256), nullable=True)
    grade = db.Column(db.Integer)
    answer = db.Column(db.String(256))

    def __init__(self, content, tag, rating, picture, grade, answer):
        self.content = content
        self.tag = tag
        self.rating = rating
        self.picture = picture
        self.grade = grade
        self.answer = answer

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self.id

    def remove(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Task.query.all()

    @staticmethod
    def get_all_reverse():
        tasks = Task.get_all()
        return tasks[::-1]

    @staticmethod
    def update_by_id(id, key, value):
        db.session.query(Task).filter(Task.id == id).update({key: value}, synchronize_session='evaluate')
        db.session.commit()

    @staticmethod
    def get_all_task_for_user(grade):
        return db.session.query(Task).filter(Task.grade == grade).all()

    @staticmethod
    def get_proc_all_tasks(grade):
        tasks = Task.get_all_task_for_user(grade)
        result = 0
        for i in tasks:
            result += i.rating
        return result
