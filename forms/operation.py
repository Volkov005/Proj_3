from flask_wtf import FlaskForm
from wtforms import SelectField, DateField
from wtforms import SubmitField, StringField


class OperationForm(FlaskForm):
    type_operation = SelectField('Тип операции', validate_choice=False)
    date_time = DateField('Дата, в формате: год(последние 2 цыфры)-месяц-день', format='%y-%m-%d')
    sum = StringField("Сумма")
    card = SelectField('Карта', validate_choice=False)
    submit = SubmitField('Применить')
