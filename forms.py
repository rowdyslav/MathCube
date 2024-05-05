from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField
from wtforms.validators import DataRequired


class ProblemTypeForm(FlaskForm):
    type = SelectField()
    submit = SubmitField("Подтвердить")

    def __init__(self, *args, problems_types, **kwargs):
        super().__init__(*args, **kwargs)
        self.type.choices = problems_types


class AnswerForm(FlaskForm):
    answer = StringField("Ответ", validators=[DataRequired()])
    submit = SubmitField("Ответить")
