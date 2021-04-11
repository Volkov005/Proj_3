from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField
from wtforms import SubmitField
from wtforms.validators import DataRequired


class Type_OperationForm(FlaskForm):
    title = StringField('Название типа', validators=[DataRequired()], render_kw={'autofocus': True})
    content = TextAreaField("Примечание")
    type_operation = SelectField('Тип', choices=[(1, 'Приход'), (2, 'Расход'), (3, 'Универсал')])
    submit = SubmitField('Сохранить')
