from flask_wtf import FlaskForm
from wtforms import SelectField
from wtforms import SubmitField


class FiltersForm(FlaskForm):
    # type_operation = SelectField('Тип операции  (1 - Приход, 2 - Расход, 3 - Универсал)', validate_choice=False)
    date = SelectField("Дата", choices=[(1, "Сначала новые"), (2, "Сначала старые")])
    type_operation = SelectField('Тип операции', choices=[(0, 'Нет'), (1, 'Приход'), (2, 'Расход')],
                                 validate_choice=False)
    card = SelectField("Карта", validate_choice=False)
    submit = SubmitField("Применить")
