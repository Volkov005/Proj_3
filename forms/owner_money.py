from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms import SubmitField
from wtforms.validators import DataRequired


class Owner_moneyForm(FlaskForm):
    title = StringField('Заголовок', validators=[DataRequired()], render_kw={'autofocus': True})
    content = TextAreaField("Содержание")
    submit = SubmitField('Применить')
