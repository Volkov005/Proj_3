from flask_wtf import FlaskForm
from wtforms import SelectField, DateField
from wtforms import SubmitField, StringField


class OperationForm(FlaskForm):
    type_operation = SelectField('Тип операции', choices=['Приход', 'Расход', 'Универсал'])
    date_time = DateField('Дата', format='%y-%m-%d')
    sum = StringField("Сумма")
    card = SelectField(u'Карта', coerce=str)
    submit = SubmitField('Применить')
