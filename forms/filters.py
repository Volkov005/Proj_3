#!/usr/bin/env python
# -*- coding: utf-8 -*-


from flask_wtf import FlaskForm
from wtforms import SelectField
from wtforms import SubmitField


class Filters1Form(FlaskForm):
    # type_operation = SelectField('Тип операции  (1 - Приход, 2 - Расход, 3 - Универсал)', validate_choice=False)
    date = SelectField(choices=[(0, "Сначала новые"), (1, "Сначала старые")], default=0)
    card = SelectField(default=0, validate_choice=False)
    type_operation_filter = SelectField(choices=[(0, 'Все'), (1, 'Сначала Приход'), (2, 'Сначала Расход'),
                                                 (3, 'Только Приход'), (4, 'Только Расход')], default=0)
    submit = SubmitField("Отфильтровать")


class FiltersForm(Filters1Form):
    form_widget_args = {
        'description': {
            'rows': 10,
        }
    }