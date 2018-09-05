from flask_wtf import FlaskForm
from wtforms import SubmitField, FileField
from wtforms.validators import DataRequired


class PhotoForm(FlaskForm):
    file = FileField('photo', validators=[DataRequired(message='Это обязательное поле.')])
    submit_photo = SubmitField('submit_photo')
