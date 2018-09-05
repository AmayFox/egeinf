from flask import render_template, redirect, request
from flask.views import MethodView
from flask_login import login_required, current_user
from web.api.models.user import User
from web.api.forms.PhotoForm import PhotoForm
from web import app, db, ALLOWED_EXTENSIONS
from werkzeug.utils import secure_filename
import os
import random


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


class AccountController(MethodView):
    @login_required
    def get(self):
        form1 = PhotoForm()
        return render_template('account.html', form1=form1)


    @login_required
    def post(self):
        form1 = PhotoForm()
        if form1.submit_photo.data and form1.validate_on_submit():
            print('hello!')
            file = request.files['file']
            if file and allowed_file(file.filename):
                code = ''.join(
                    [random.choice(list('123456789qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM')) for x in
                     range(8)])
                filename = code + current_user.code + secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                User.update_by_login(current_user.login, 'photo', filename)
                return redirect('/account')
            return render_template('account.html', form1=form1)
        return render_template('account.html', form1=form1)
