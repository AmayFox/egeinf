from flask import redirect
from flask_login import login_required, current_user
from web.api.models.progAnswers import ProgAnswers
from web.api.models.score import Score
from web.api.models.attempt import Attempt
from web.api.models.task import Task
from web import db
from flask.views import MethodView


class GoodProgramController(MethodView):
    @login_required
    def get(self, id):
        if current_user.role != 'admin':
            return redirect('/error/rights')

        progAnswer = db.session.query(ProgAnswers).filter(ProgAnswers.id == id).first()
        task = db.session.query(Task).filter(Task.id == progAnswer.task_id).first()

        ProgAnswers.update_by_id(progAnswer.id, 'status', 'Success')

        if db.session.query(Attempt).filter(Attempt.author == current_user.login).filter(Attempt.task_id == task.id).filter(Attempt.status == 'Success').first():
            return redirect('/tasks')
        attempt = Attempt.query.filter_by(task_id=task.id).filter_by(author=progAnswer.author).update(dict(status='Success'))
        db.session.commit()

        score = Score(task.rating, current_user.login)
        score.save()
        return redirect('/tasks')


class BadProgramController(MethodView):
    @login_required
    def get(self, id):
        if current_user.role != 'admin':
            return redirect('/error/rights')

        progAnswer = db.session.query(ProgAnswers).filter(ProgAnswers.id == id).first()
        task = db.session.query(Task).filter(Task.id == progAnswer.task_id).first()

        ProgAnswers.update_by_id(id, 'status', 'Failed')
        Attempt.query.filter_by(task_id=task.id).filter_by(author=current_user.login).update(dict(status='Failed'))
        db.session.commit()

        return redirect('/tasks')
