from flask_login import login_required, current_user
from flask.views import MethodView
from flask import render_template, redirect
from web.api.models.user import User
from web import db
from web.api.models.task import Task
from web.api.models.score import Score


class ShowOtherUserController(MethodView):
    @login_required
    def get(self, login):
        if login == current_user.login:
            return redirect('/account')

        user = db.session.query(User).filter(User.login == login).first()
        maxscore = Task.get_proc_all_tasks(user.grade)
        score = Score.get_final_score(user.login)
        if score == 0:
            return render_template('user.html', user=user, score=0, procent=0)

        procent = int((maxscore / score) * 100)
        return render_template('user.html', user=user, score=score, procent=procent)
