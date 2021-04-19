#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime

from flask_wtf import FlaskForm
from wtforms import SelectField, DateField
from wtforms import SubmitField
from wtforms.validators import ValidationError


class FiltersForm(FlaskForm):
    # type_operation = SelectField('Тип операции  (1 - Приход, 2 - Расход, 3 - Универсал)', validate_choice=False)
    date = SelectField(choices=[(0, "Сначала новые"), (1, "Сначала старые")], default=0)
    card = SelectField(default=0, validate_choice=False)
    type_operation_filter = SelectField(choices=[(0, 'Все'), (1, 'Сначала Приход'), (2, 'Сначала Расход'),
                                                 (3, 'Только Приход'), (4, 'Только Расход')], default=0)
    first_date = DateField(format='%d/%m/%Y')
    last_date = DateField(format='%d/%m/%Y')
    submit = SubmitField("Отфильтровать")

    def validate_last_date(form, field):
        if form.first_date.data and field.data:
            if field.data < form.first_date.data:
                raise ValidationError("Последняя дата не должна быть раньше начальной!!")
