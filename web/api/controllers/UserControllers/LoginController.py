from flask import render_template, redirect
from flask.views import MethodView
from web import db
from web.api.models.user import User
from web.api.forms.LoginForm import LoginForm
from hashlib import sha256
from flask_login import login_user


class LoginController(MethodView):
    def get(self):
        form = LoginForm()
        return render_template('login.html', form=form)

    def post(self):
        form = LoginForm()
        if form.validate_on_submit():
            password = sha256(form.password.data.encode()).hexdigest()
            user_count = User.query.filter(User.login == form.login.data).filter(User.password == password)
            if user_count.count():
                user = db.session.query(User).filter(User.login == form.login.data).first()
                login_user(user)
                return redirect('/')
            return render_template('login.html', form=form, error_text='Неправильный логин или пароль.')
        return render_template('login.html', form=form)
