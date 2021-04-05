import datetime

from flask_wtf import FlaskForm
from wtforms import SelectField, DateField
from wtforms import SubmitField, StringField


class OperationForm(FlaskForm):
    type_operation = SelectField('Тип операции  (1 - Приход, 2 - Расход, 3 - Универсал)', validate_choice=False)
    date_time = DateField('Дата, в формате: год-месяц-день', format='%y-%m-%d', default=datetime.date.today())
    card = SelectField('Карта', validate_choice=False)
    sum = StringField("Сумма", default=0)
    card_from = SelectField('Карта', validate_choice=False)
    card_to = SelectField('Карта', validate_choice=False)
    submit = SubmitField('Применить')
