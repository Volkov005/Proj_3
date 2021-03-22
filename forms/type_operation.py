from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField
from wtforms import SubmitField
from wtforms.validators import DataRequired


class Type_OperationForm(FlaskForm):
    title = StringField('Заголовок', validators=[DataRequired()])
    content = TextAreaField("Содержание")
    type_operation = SelectField('Тип', choices=['Приход', 'Расход', 'Универсал'])
    submit = SubmitField('Применить')
