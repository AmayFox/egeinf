from flask import render_template, redirect
from flask.views import MethodView
from flask_login import current_user, login_required
from web.api.models.score import Score
from web.api.models.user import User
from web.api.models.task import Task


class ScoreboardController(MethodView):
    @login_required
    def get(self):
        # Сам скорборд, обычная таблица
        all_scores = list()

        users = User.get_all_one_grade(current_user.grade)
        summa = Task.get_proc_all_tasks(current_user.grade)
        for i in users:
            procent = 0
            final_score = Score.get_final_score(i.login)
            if final_score != 0:
                procent = int((final_score / summa) * 100)
            need_save = str(final_score) + '|' + i.login + '|' + str(procent) + '%'
            all_scores.append(need_save)

        new_list = list()
        final = list()
        for i in range(len(all_scores)):
            new_list = all_scores[i].split('|')
            final.append(new_list)

        final = sorted(final, reverse=True)
        return render_template('scoreboard.html', final=final)


class Scoreboard11Controller(MethodView):
    @login_required
    def get(self):
        if current_user.role != 'admin':
            return redirect('/error/rights')

        # Сам скорборд, обычная таблица
        all_scores = list()

        users = User.get_all_one_grade(11)
        summa = Task.get_proc_all_tasks(11)
        for i in users:
            procent = 0
            final_score = Score.get_final_score(i.login)
            if final_score != 0:
                procent = int((final_score / summa) * 100)
            need_save = str(final_score) + '|' + i.login + '|' + str(procent) + '%'
            all_scores.append(need_save)

        new_list = list()
        final = list()
        for i in range(len(all_scores)):
            new_list = all_scores[i].split('|')
            final.append(new_list)

        final = sorted(final, reverse=True)
        return render_template('scoreboard_11.html', final=final)


class Scoreboard9Controller(MethodView):
    @login_required
    def get(self):
        if current_user.role != 'admin':
            return redirect('/error/rights')

        # Сам скорборд, обычная таблица
        all_scores = list()

        users = User.get_all_one_grade(9)
        summa = Task.get_proc_all_tasks(9)
        for i in users:
            procent = 0
            final_score = Score.get_final_score(i.login)
            if final_score != 0:
                procent = int((final_score / summa) * 100)
            need_save = str(final_score) + '|' + i.login + '|' + str(procent) + '%'
            all_scores.append(need_save)

        new_list = list()
        final = list()
        for i in range(len(all_scores)):
            new_list = all_scores[i].split('|')
            final.append(new_list)

        final = sorted(final, reverse=True)
        return render_template('scoreboard_9.html', final=final)
