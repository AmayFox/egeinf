from flask import render_template, redirect, request
from flask.views import MethodView
from flask_login import login_required, current_user
from web.api.models.task import Task
from web.api.models.answer import Answer
from web.api.models.progAnswers import ProgAnswers
from web import db, ALLOWED_EXTENSIONS_FOR_PROGRAMMING, app
import random
import os
from werkzeug.utils import secure_filename
from web.api.models.score import Score
import datetime
from web.api.models.attempt import Attempt


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS_FOR_PROGRAMMING


def my_shuffle(array):
    random.shuffle(array)
    return array


class SolveTaskController(MethodView):
    @login_required
    def get(self, id):
        task = db.session.query(Task).filter(Task.id == id).first()
        answers = Answer.get_all_answers_from_task(id)
        checking = ProgAnswers.get_all_reverse()

        oneAnswer = False
        progAnswer = False
        fourAnswer = False
        four_shuffle_answers = list()

        if len(answers) == 1:
            oneAnswer = True
        elif len(answers) == 0 and task.answer == 'PROG':
            progAnswer = True
        elif len(answers) == 4:
            fourAnswer = True
            answers_contnet = list()
            for i in range(4):
                answers_contnet.append(answers[i].content)
            four_shuffle_answers = my_shuffle(answers_contnet)

        return render_template('task.html', task=task, four_shuffle_answers=four_shuffle_answers,
                               fourAnswer=fourAnswer, oneAnswer=oneAnswer, progAnswer=progAnswer, checking=checking)

    @login_required
    def post(self, id):
        task = db.session.query(Task).filter(Task.id == id).first()
        answers = Answer.get_all_answers_from_task(id)
        checking = ProgAnswers.get_all_reverse()

        oneAnswer = False
        progAnswer = False
        fourAnswer = False
        four_shuffle_answers = list()

        if len(answers) == 1:
            oneAnswer = True
        elif len(answers) == 1 and task.answer == 'PROG TASK':
            progAnswer = True
        elif len(answers) == 4:
            fourAnswer = True
            answers_contnet = list()
            for i in range(4):
                answers_contnet.append(answers[i].content)
            four_shuffle_answers = my_shuffle(answers_contnet)

        if 'submit-one-answer' in request.form:
            text = request.form['answer-one']
            if task.answer == text:
                if db.session.query(Attempt).filter(Attempt.author == current_user.login).filter(Attempt.task_id == task.id).filter(Attempt.status == 'Success').first():
                    return render_template('task.html', task=task, four_shuffle_answers=four_shuffle_answers,
                                           fourAnswer=fourAnswer, oneAnswer=oneAnswer, progAnswer=progAnswer,
                                           success_text='Ответ правильный! Однако Вы уже сдавали это задание.')
                attempt = Attempt(current_user.login, task.id, 'Success')
                attempt.save()

                score = Score(task.rating, current_user.login)
                score.save()
                return render_template('task.html', task=task, four_shuffle_answers=four_shuffle_answers,
                                       fourAnswer=fourAnswer, oneAnswer=oneAnswer, progAnswer=progAnswer,
                                       success_text='Задание успешно сдано!')
            else:
                return render_template('task.html', task=task, four_shuffle_answers=four_shuffle_answers,
                                       fourAnswer=fourAnswer, oneAnswer=oneAnswer, progAnswer=True,
                                       error_text='Ошибка! Проверьте все еще раз.')

        if 'submit-four-answer' in request.form:
            value = request.form['answer-four']
            if value == task.answer:
                if db.session.query(Attempt).filter(Attempt.author == current_user.login).filter(Attempt.task_id == task.id).filter(Attempt.status == 'Success').first():
                    return render_template('task.html', task=task, four_shuffle_answers=four_shuffle_answers,
                                           fourAnswer=fourAnswer, oneAnswer=oneAnswer, progAnswer=progAnswer,
                                           success_text='Ответ правильный! Однако Вы уже сдавали это задание.')
                attempt = Attempt(current_user.login, task.id, 'Success')
                attempt.save()

                score = Score(task.rating, current_user.login)
                score.save()
                return render_template('task.html', task=task, four_shuffle_answers=four_shuffle_answers,
                                       fourAnswer=fourAnswer, oneAnswer=oneAnswer, progAnswer=progAnswer,
                                       success_text='Задание успешно сдано!')
            else:
                return render_template('task.html', task=task, four_shuffle_answers=four_shuffle_answers,
                                       fourAnswer=fourAnswer, oneAnswer=oneAnswer, progAnswer=progAnswer,
                                       error_text='Ошибка! Проверьте все еще раз.')

        if 'submit-prog-task' in request.form:
            file = request.files.get('file')
            filename = '0'
            if file is not None and allowed_file(file.filename):
                code = ''.join(
                    [random.choice(list('123456789qwertyuiopasdfghjkzxcvbnmQWERTYUOPASDFGHJKLZXCVBNM')) for x in
                     range(12)])
                filename = code + current_user.code + secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER_FOR_RPOG'], filename))

                time = datetime.datetime.now().strftime("%H:%M %d.%m.%Y")

                answer = ProgAnswers(filename, current_user.login, task.id, time)
                answer.save()

                attempt = Attempt(current_user.login, task.id, 'Check')
                attempt.save()
                return render_template('task.html', task=task, four_shuffle_answers=four_shuffle_answers,
                                       fourAnswer=fourAnswer, oneAnswer=oneAnswer, progAnswer=progAnswer,
                                       success_text='Задание принято на проверку!', checking=checking)
            else:
                return render_template('task.html', task=task, four_shuffle_answers=four_shuffle_answers,
                                       fourAnswer=fourAnswer, oneAnswer=oneAnswer, progAnswer=progAnswer,
                                       error_text='Что-то пошло не так. Проверьте расширение файла.', checking=checking)

        if 'que-to-teacher' in request.form:
            content = request.form['textarea-to-teacher']

            time = datetime.datetime.now().strftime("%H:%M %d.%m.%Y")
            dash = Dashboard(content, task.id, current_user.login, time, current_user.grade)
            dash.save()
            return render_template('task.html', task=task, four_shuffle_answers=four_shuffle_answers,
                                   fourAnswer=fourAnswer, oneAnswer=oneAnswer, progAnswer=progAnswer,
                                   success_text='Ваш вопрос отправлен учителю!', checking=checking)

        return render_template('task.html', task=task, four_shuffle_answers=four_shuffle_answers,
                               fourAnswer=fourAnswer, oneAnswer=oneAnswer, progAnswer=progAnswer, checking=checking)
