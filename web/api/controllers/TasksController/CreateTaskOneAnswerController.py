from flask import render_template, redirect, request
from flask.views import MethodView
from flask_login import login_required, current_user
from web.api.forms.CreateTaskForm import CreateTaskOneAnswerForm
from web import app, ALLOWED_EXTENSIONS
import os
import random
from werkzeug.utils import secure_filename
from web.api.models.task import Task
from web.api.models.answer import Answer


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


class CreateTaskOneAnswerController(MethodView):
    @login_required
    def get(self):
        if current_user.role != 'admin':
            return redirect('/error/right')

        form = CreateTaskOneAnswerForm()
        return render_template('createTaskOneAnswer.html', form=form)

    @login_required
    def post(self):
        if current_user.role != 'admin':
            return redirect('/error/right')

        form = CreateTaskOneAnswerForm()
        if form.validate_on_submit():
            grade = request.form['inlineRadioOptions']
            rating = request.form['select-rating']

            file = request.files.get('file')
            filename = '0'
            if file is not None and allowed_file(file.filename):
                code = ''.join(
                    [random.choice(list('123456789qwertyuiopasdfghjkzxcvbnmQWERTYUOPASDFGHJKLZXCVBNM')) for x in
                     range(12)])
                filename = code + current_user.code + secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            task = Task(form.content.data, form.tag.data, int(rating), filename, int(grade), form.answer.data)
            task.save()

            answer = Answer(form.answer.data, True, task.id)
            answer.save()
            return redirect('/tasks')
        return render_template('createTaskOneAnswer.html', form=form)
