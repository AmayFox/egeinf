from flask import render_template, redirect, request
from flask.views import MethodView
from hashlib import sha256
from web.api.forms.EditProfileInfoForms import EditNameForm, EditEmailForm, EditPasswordForm
from web.api.forms.PhotoForm import PhotoForm
from web.api.models.user import User
import random
from web import ALLOWED_EXTENSIONS, app
import os
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user
from web import db


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


class EditNameController(MethodView):
    @login_required
    def get(self):
        form = EditNameForm()
        return render_template('editing/editUserName.html', form=form)

    @login_required
    def post(self):
        form = EditNameForm()
        if form.validate_on_submit():
            login = current_user.login
            User.update_by_login(login, 'name', form.name.data)
            return render_template('editing/editUserName.html', form=form, success_text='Ваше имя успешно изменено!')
        return render_template('editing/editUserName.html', form=form)


class EditEmailController(MethodView):
    @login_required
    def get(self):
        form = EditEmailForm()
        return render_template('editing/editUserEmail.html', form=form)

    @login_required
    def post(self):
        form = EditEmailForm()
        if form.validate_on_submit():
            login = current_user.login
            password_form = sha256(form.password.data.encode()).hexdigest()
            user_count = User.query.filter(User.login == current_user.login).filter(User.password == password_form)
            if user_count.count() and not db.session.query(User).filter(User.email == form.email.data).first():
                User.update_by_login(login, 'email', form.email.data)
                return render_template('editing/editUserEmail.html', form=form, success_text='Ваша почта успешно изменена!')
            # Проверка на уникальность почты

            if db.session.query(User).filter(User.email == form.email.data).first():
                return render_template('editing/editUserEmail.html', form=form,
                                       error_text='Пользователь с такой почтой уже существует.')
            else:
                return render_template('editing/editUserEmail.html', form=form, error_text='Вы ввели неправильный пароль.')
        return render_template('editing/editUserEmail.html', form=form)


class EditPasswordController(MethodView):
    @login_required
    def get(self):
        form = EditPasswordForm()
        return render_template('editing/editUserPassword.html', form=form)

    @login_required
    def post(self):
        form = EditPasswordForm()
        if form.validate_on_submit():
            login = current_user.login
            password_form = sha256(form.old_password.data.encode()).hexdigest()
            user_count = User.query.filter(User.login == current_user.login).filter(User.password == password_form)
            if user_count.count():
                secret_pass = sha256(form.new_password.data.encode()).hexdigest()
                User.update_by_login(login, 'password', secret_pass)
                return render_template('editing/editUserPassword.html', form=form, success_text='Пароль успешно изменен!')
            return render_template('editing/editUserPassword.html', form=form, error_text='Вы ввели неправильный старый пароль.')
        return render_template('editing/editUserPassword.html', form=form)


class EditAvatarController(MethodView):
    @login_required
    def get(self):
        form = PhotoForm()
        return render_template('editing/editUserAvatar.html', form=form)

    @login_required
    def post(self):
        form = PhotoForm()
        if form.submit_photo.data and form.validate_on_submit():
            file = request.files['file']
            if file and allowed_file(file.filename):
                code = ''.join([random.choice(list('123456789qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM')) for x in range(8)])
                filename = code + current_user.code + secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

                path_to_deleting_file = 'web/static/photos/uploads/' + str(current_user.photo)
                os.remove(path_to_deleting_file)
                User.update_by_login(current_user.login, 'photo', filename)
                return redirect('/account')
            return render_template('editing/editUserAvatar.html', form=form, error_text='Что-то пошло не так. Попробуйте еще раз.')
        return render_template('editing/editUserAvatar.html', form=form)
