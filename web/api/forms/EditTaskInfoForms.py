from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired


class EditTaskContentForm(FlaskForm):
    content = TextAreaField('content', validators=[DataRequired(message='Это обязательное поле.')])


class EditTaskTagForm(FlaskForm):
    tag = StringField('tag', validators=[DataRequired(message='Это обязательное поле.')])
