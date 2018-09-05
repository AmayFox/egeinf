from web.api.models.answer import Answer
from web.api.models.task import Task
from flask import render_template, redirect, request
from web.api.forms.CreateTaskForm import CreateTaskFourAnswersForm
from flask.views import MethodView
from flask_login import login_required, current_user
from web import app, ALLOWED_EXTENSIONS
import os
from werkzeug.utils import secure_filename
import random


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


class CreateTaskFourAnswersController(MethodView):
    @login_required
    def get(self):
        if current_user.role != 'admin':
            return redirect('/error/right')

        form = CreateTaskFourAnswersForm()
        return render_template('createTaskFourAnswers.html', form=form)

    @login_required
    def post(self):
        if current_user.role != 'admin':
            return redirect('/error/right')

        form = CreateTaskFourAnswersForm()
        if form.validate_on_submit():
            grade = request.form['inlineRadioOptions']
            rating = request.form['select-rating']

            file = request.files.get('file')
            print(file)
            filename = '0'
            if file is not None and allowed_file(file.filename):
                code = ''.join(
                    [random.choice(list('123456789qwertyuiopasdfghjkzxcvbnmQWERTYUOPASDFGHJKLZXCVBNM')) for x in
                     range(12)])
                filename = code + current_user.code + secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            task = Task(form.content.data, form.tag.data, int(rating), filename, int(grade), form.answer1.data)
            task.save()

            right_answer = Answer(form.answer1.data, True, task.id)
            right_answer.save()

            answer2 = Answer(form.answer2.data, False, task.id)
            answer2.save()

            answer3 = Answer(form.answer3.data, False, task.id)
            answer3.save()

            answer4 = Answer(form.answer4.data, False, task.id)
            answer4.save()

            return redirect('/tasks')
        return render_template('createTaskFourAnswers.html', form=form)
