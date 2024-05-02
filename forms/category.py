from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from wtforms.validators import DataRequired

class ProductForm(FlaskForm):
    type = SelectField('Тип задачи', choices=[(0, '0')])
    submit = SubmitField('Подтвердить')

    def __init__(self, *args, data=[(1, '1')], **kwargs):
        super().__init__(*args, **kwargs)
        self.type.choices = data
