import datetime
import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Operations(SqlAlchemyBase):
    __tablename__ = 'operations'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    created_date = sqlalchemy.Column(sqlalchemy.Date,
                                     default=datetime.date.today())
    type_operation_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('type_of_operation.id'))
    content = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("users.id"))
    user = orm.relation('User')
