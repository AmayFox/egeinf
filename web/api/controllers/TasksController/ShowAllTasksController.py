from flask import render_template, redirect
from flask.views import MethodView
from flask_login import login_required, current_user
from web.api.models.task import Task


class ShowAllTasksController(MethodView):
    def get(self):
        if current_user.role != 'admin':
            return redirect('/error/rights')

        tasks = Task.get_all_reverse()
        return render_template('all_tasks.html', tasks=tasks)
