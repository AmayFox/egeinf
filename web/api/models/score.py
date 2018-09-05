from web import db


class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer)
    login = db.Column(db.String(256))

    def __init__(self, score, login):
        self.score = score
        self.login = login

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self.id

    @staticmethod
    def get_all():
        return Score.query.all()

    @staticmethod
    def get_final_score(login):
        final_score = 0
        finishes = Score.get_all()
        for f in finishes:
            if f.login == login:
                final_score += f.score
        return final_score
