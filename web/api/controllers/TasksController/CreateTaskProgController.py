from web.api.models.answer import Answer
from web.api.models.task import Task
from flask import render_template, redirect, request
from flask.views import MethodView
from flask_login import login_required, current_user
from web import app, ALLOWED_EXTENSIONS
import os
from web.api.forms.CreateTaskForm import CreateTaskProgForm
from werkzeug.utils import secure_filename
import random


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


class CreateTaskProgController(MethodView):
    @login_required
    def get(self):
        if current_user.role != 'admin':
            return redirect('/error/right')

        form = CreateTaskProgForm()
        return render_template('createTaskProg.html', form=form)

    @login_required
    def post(self):
        if current_user.role != 'admin':
            return redirect('/error/right')

        form = CreateTaskProgForm()
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

            task = Task(form.content.data, form.tag.data, int(rating), filename, int(grade), 'PROG')
            task.save()
            return redirect('/tasks')
        return render_template('createTaskProg.html', form=form)
