from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, SubmitField, EmailField, PasswordField
from wtforms.validators import DataRequired

class AnswerForm(FlaskForm):
    answer = StringField('Ответ', validators=[DataRequired()])
    submit = SubmitField('Ответить')
