import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class Sales(SqlAlchemyBase):
    __tablename__ = 'sales'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey('users.id'))
    list_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey('lists.id'))
    item_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey('items.id'))

    list = orm.relationship('Lists')
    user = orm.relationship('Users')
    item = orm.relationship('Items')
    state = sqlalchemy.Column(sqlalchemy.Boolean)

