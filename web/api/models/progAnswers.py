from web import db


class ProgAnswers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(256))
    author = db.Column(db.String(256))
    task_id = db.Column(db.Integer)
    time = db.Column(db.String(256))
    status = db.Column(db.String(256))

    def __init__(self, filename, author, task_id, time, status='Check'):
        self.filename = filename
        self.author = author
        self.task_id = task_id
        self.time = time
        self.status = status

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self.id

    @staticmethod
    def get_all():
        return ProgAnswers.query.all()

    @staticmethod
    def get_all_reverse():
        answers = ProgAnswers.get_all()
        return answers[::-1]

    @staticmethod
    def get_all_answers_from_task(id):
        tasks = db.session.query(ProgAnswers).filter(ProgAnswers.task_id == id).all()
        return tasks[::-1]

    @staticmethod
    def update_by_id(id, key, value):
        db.session.query(ProgAnswers).filter(ProgAnswers.id == id).update({key: value}, synchronize_session='evaluate')
        db.session.commit()
