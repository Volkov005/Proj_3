from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms import SubmitField
from wtforms.validators import DataRequired


class CardForm(FlaskForm):
    title = StringField('Название карты', validators=[DataRequired()], render_kw={'autofocus': True})
    content = TextAreaField("Примечание")
    balance = TextAreaField('Изменить баланс')
    submit = SubmitField('Сохранить')
