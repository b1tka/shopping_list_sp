import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class Users(SqlAlchemyBase):
    __tablename__ = 'users'

    users_to_groups_table = sqlalchemy.Table(
        'users_to_groups',
        SqlAlchemyBase.metadata,
        sqlalchemy.Column('group', sqlalchemy.Integer, sqlalchemy.ForeignKey('groups.id')),
        sqlalchemy.Column('user', sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'))
    )

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    tg_user_id = sqlalchemy.Column(sqlalchemy.Integer, unique=True)
    chat_id = sqlalchemy.Column(sqlalchemy.Integer)
    nickname = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    personal_time = sqlalchemy.Column(sqlalchemy.Time)

    admin = orm.relationship('Group', back_populates='admin')
