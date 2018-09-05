from flask import render_template, redirect
from flask.views import MethodView
from flask_login import current_user, login_required
from web.api.models.task import Task
from web.api.models.attempt import Attempt
from web.api.models.user import User
from web.api.models.score import Score


class TasksController(MethodView):
    @login_required
    def get(self):
        if current_user.grade == 0:
            return redirect('/account')
        tasks = Task.get_all_task_for_user(current_user.grade)
        attempts = Attempt.get_all()

        if len(attempts) == 0:
            return render_template('tasks.html', actual=tasks)

        finished = list()
        checking = list()
        for task in tasks:
            for att in attempts:
                if task.id == att.task_id and att.status == 'Check' and att.author == current_user.login:
                    checking.append(task)
                    break
                elif task.id == att.task_id and att.status == 'Success' and att.author == current_user.login:
                    finished.append(task)
                    break

        actual = list(set(tasks) - set(finished))
        actual = set(actual) - set(checking)

        # Сам скорборд, обычная таблица
        all_scores_11 = list()

        users11 = User.get_all_one_grade(11)
        for i in users11:
            final_score = Score.get_final_score(i.login)
            need_save = str(final_score) + '|' + i.login
            all_scores_11.append(need_save)

        new_list = list()
        final11 = list()
        for i in range(len(all_scores_11)):
            new_list = all_scores_11[i].split('|')
            final11.append(new_list)

        final11 = sorted(final11, reverse=True)

        # Сам скорборд, обычная таблица
        all_scores_9 = list()

        users9 = User.get_all_one_grade(9)
        for i in users9:
            final_score = Score.get_final_score(i.login)
            need_save = str(final_score) + '|' + i.login
            all_scores_9.append(need_save)

        new_list = list()
        final9 = list()
        for i in range(len(all_scores_9)):
            new_list = all_scores_9[i].split('|')
            final9.append(new_list)

        final9 = sorted(final9, reverse=True)
        return render_template('tasks.html', actual=actual, finished=finished, checking=checking, final9=final9[:3],
                               final11=final11[:3])
