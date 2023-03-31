import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


users_to_groups_table = sqlalchemy.Table(
    'users_to_groups',
    SqlAlchemyBase.metadata,
    sqlalchemy.Column('group', sqlalchemy.Integer, sqlalchemy.ForeignKey('groups.id')),
    sqlalchemy.Column('user', sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'))
)


class Group(SqlAlchemyBase):
    __tablename__ = 'groups'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    code = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    admin_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'))
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    admin = orm.relationship('Users')
    members = orm.relationship('Users', secondary='users_to_groups', backref='groups')
    lists = orm.relationship('Lists', back_populates='group')