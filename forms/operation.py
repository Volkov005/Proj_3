from flask_wtf import FlaskForm
from wtforms import SelectField, DateField
from wtforms import SubmitField, StringField


class OperationForm(FlaskForm):
    type_operation = SelectField('Тип операции')
    date_time = DateField('Дата, в формате: год(последние 2 цыфры)-месяц-день', format='%y-%m-%d')
    sum = StringField("Сумма")
    card = SelectField('Карта')
    submit = SubmitField('Применить')
