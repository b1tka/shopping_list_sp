import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class Lists(SqlAlchemyBase):
    __tablename__ = 'lists'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    group_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('groups.id'))


    group = orm.relationship('Group')
    sales = orm.relationship('Sales', back_populates='list')