import sqlalchemy
from .db_session import SqlAlchemyBase


class Lists(SqlAlchemyBase):
    __tablename__ = 'lists'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    item = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    state = sqlalchemy.Column(sqlalchemy.Boolean())
