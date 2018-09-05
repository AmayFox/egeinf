from flask import render_template, redirect
from flask_login import login_required, current_user
from flask.views import MethodView
from web import APP_ROOT


class ShowProgAnswerController(MethodView):
    @login_required
    def get(self, filename):
        if current_user.role != 'admin':
            return redirect('/error/rights')

        file_path = APP_ROOT + '/static/tasks/' + filename
        f = open(file_path)
        return render_template('showProgAnswer.html', file=f)
