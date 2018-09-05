from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, FileField
from wtforms.validators import DataRequired


class CreateTaskOneAnswerForm(FlaskForm):
    content = TextAreaField(label='Вопрос', validators=[DataRequired(message='Это обязательное поле.')])
    file = FileField('photo')
    answer = StringField(label='Вариант ответа', validators=[DataRequired(message='Это обязательное поле.')])
    tag = StringField('Тег', validators=[DataRequired(message='Это обязательное поле.')])
    submit = SubmitField('Создать таск')


class CreateTaskFourAnswersForm(FlaskForm):
    content = TextAreaField(label='Вопрос', validators=[DataRequired(message='Это обязательное поле.')])
    file = FileField('photo')
    answer1 = StringField(label='Вариант ответа1', validators=[DataRequired(message='Это обязательное поле.')])
    answer2 = StringField(label='Вариант ответа2', validators=[DataRequired(message='Это обязательное поле.')])
    answer3 = StringField(label='Вариант ответа3', validators=[DataRequired(message='Это обязательное поле.')])
    answer4 = StringField(label='Вариант ответа4', validators=[DataRequired(message='Это обязательное поле.')])
    tag = StringField('Тег', validators=[DataRequired(message='Это обязательное поле.')])
    submit = SubmitField('Создать таск')


class CreateTaskProgForm(FlaskForm):
    content = TextAreaField(label='Вопрос', validators=[DataRequired(message='Это обязательное поле.')])
    file = FileField('photo')
    tag = StringField('Тег', validators=[DataRequired(message='Это обязательное поле.')])
