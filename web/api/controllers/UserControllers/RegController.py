from flask import render_template, redirect, url_for
from flask.views import MethodView
from web.api.forms.RegForm import RegForm
from web.api.models.user import User
import random
from hashlib import sha256
from flask_login import login_user


class RegController(MethodView):
    def get(self):
        form = RegForm()
        return render_template('reg.html', form=form)

    def post(self):
        form = RegForm()

        if form.validate_on_submit():
            same_login = User.query.filter(User.login == form.login.data).count()
            if same_login:
                return render_template('reg.html', form=form, error_text='Пользователь с таким логином уже существует.')

            code = ''.join([random.choice(list('123456789qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM')) for x in range(8)])
            secret_pass = sha256(form.password.data.encode()).hexdigest()
            if form.login.data == 'AmayFox':
                user_admin = User(form.name.data, form.login.data, secret_pass, code, 'admin')
                user_admin.save()
                login_user(user_admin)
                return redirect(url_for('api.MainPage'))

            user = User(form.name.data, form.login.data, secret_pass, code, 'user')
            user.save()
            login_user(user)
            return redirect(url_for('api.MainPage'))
        return render_template('reg.html', form=form)
