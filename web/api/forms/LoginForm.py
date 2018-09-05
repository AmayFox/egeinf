from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    login = StringField('login', validators=[DataRequired(message='Это обязательное поле.')])
    password = StringField('password', validators=[DataRequired(message='Это обязательное поле.')])