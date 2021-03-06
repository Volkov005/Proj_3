import datetime

from flask_wtf import FlaskForm
from wtforms import SelectField, DateField, TextAreaField, FloatField
from wtforms import SubmitField
from wtforms.validators import NumberRange


class OperationForm(FlaskForm):
    type_operation = SelectField('Тип операции  (1 - Приход, 2 - Расход, 3 - Универсал)', validate_choice=False)
    date_time = DateField("Дата операции (ДД/ММ/ГГГГ)", format='%d/%m/%Y', default=datetime.date.today(),
                          render_kw={'autofocus': True})
    card = SelectField("Карта", validate_choice=False)
    sum = FloatField("Сумма", validators=[NumberRange(min=0.01,
                                                      message=';Проверьте формат ввода и,'
                                                              ' что ваше число больше минимального (0.01)')])
    content = TextAreaField("Примечание")
    card_from = SelectField("Карта", validate_choice=False)
    card_to = SelectField("Карта", validate_choice=False)
    submit = SubmitField("Применить")
