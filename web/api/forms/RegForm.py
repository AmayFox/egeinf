from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, ValidationError
from wtforms.validators import DataRequired, Length, EqualTo
import re


pattern = r'^[A-Za-z0-9_-]*$'


def latinica_only(form, field):
    if not re.match(pattern, str(field.data)):
        raise ValidationError('Символы могут включать в себя латинские буквы, номера, или - _')


class RegForm(FlaskForm):
    name = StringField(label='Имя', validators=[DataRequired(message='Это обязательное поле.')])
    login = StringField(label='Логин', validators=[DataRequired(message='Это обязательное поле.'), latinica_only])
    password = PasswordField(label='Придумайте пароль', validators=[DataRequired(message='Это обязательное поле.'),
                                                                    Length(8, message='Количество символов должно превышать 8.')])
    confirmpass = PasswordField(label='Пароль для подтверждения',
                                validators=[DataRequired(message='Это обязательное поле.'),
                                            Length(8, message='Количество символов должно превышать 8.'),
                                            EqualTo('password', message='Пароли должны совпадать.')])
