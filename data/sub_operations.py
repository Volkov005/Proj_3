import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Sub_operation(SqlAlchemyBase):
    __tablename__ = 'sub_operations'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    id_operation = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('operations.id'))
    # id_owner = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('owner_money.id'))
    id_cards = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('cards.id'))
    prihod = sqlalchemy.Column(sqlalchemy.Integer)
    rashod = sqlalchemy.Column(sqlalchemy.Integer)

    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("users.id"))
    user = orm.relation('User')
