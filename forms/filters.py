from flask_wtf import FlaskForm
from wtforms import SelectField
from wtforms import SubmitField


class FiltersForm(FlaskForm):
    # type_operation = SelectField('��� ��������  (1 - ������, 2 - ������, 3 - ���������)', validate_choice=False)
    date = SelectField("����", choices=[(1, "������� �����"), (2, "������� ������")])
    type_operation = SelectField('��� ��������', choices=[(0, '���'), (1, '������'), (2, '������')],
                                 validate_choice=False)
    card = SelectField("�����", validate_choice=False)
    submit = SubmitField("���������")
