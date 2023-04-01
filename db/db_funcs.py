from sqlalchemy.exc import IntegrityError
from random import choices
from string import ascii_letters

from data import db_session
from data.users import Users
from data.group import Group
from data.lists import Lists


def add_user_to_db_table_user(username, tg_user_id, chat_id):
    db_sess = db_session.create_session()
    if db_sess.query(Users).filter(Users.tg_user_id == tg_user_id).first():
        print('ye')
        return None
    user = Users()
    user.nickname = username
    user.tg_user_id = tg_user_id
    user.chat_id = chat_id
    db_sess.add(user)
    db_sess.commit()
    db_sess.close()


def create_new_group(admin_id, name):
    db_sess = db_session.create_session()
    user = db_sess.query(Users).filter(Users.tg_user_id == admin_id).first()
    group = Group()
    group.code = ''.join(choices(list(ascii_letters), k=10))
    group.name = name
    group.admin_id = user.id
    group.members.append(user)
    db_sess.add(group)
    db_sess.commit()
    db_sess.close()


def join_to_group(group_code, user_id):
    db_sess = db_session.create_session()
    group = db_sess.query(Group).filter(Group.code == group_code).first()
    if not group:
        return None
    user = db_sess.query(Users).filter(Users.tg_user_id == user_id).first()
    if user in group.members:
        return 2
    group.members.append(user)
    name = group.name
    db_sess.commit()
    db_sess.close()
    return name


def get_group_by_user_id(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(Users).filter(Users.tg_user_id == user_id).first()
    return user.group[0].id


def get_chat_id_by_user_id(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(Users).filter(Users.tg_user_id == user_id).first()
    return user.chat_id


def get_group_name(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(Users).filter(Users.tg_user_id == user_id).first()
    return user.group[0].name


def get_actual_lists(group_id):
    db_sess = db_session.create_session()
    group = db_sess.query(Group).filter(Group.id == group_id).first()
    return group.lists


def get_name_list_by_list_id(list_id):
    db_sess = db_session.create_session()
    list = db_sess.query(Lists).filter(Lists.id == list_id).first()
    return list.name


def create_new_list(group_id, name_list):
    db_sess = db_session.create_session()
    list = Lists()
    list.group_id = group_id
    list.name = name_list
    db_sess.add(list)
    db_sess.commit()


def leave_from_group(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(Users).filter(Users.tg_user_id == user_id).first()
    print('AAAAAAAAAAAAAAAAAAAA', user.group[0])
    user.group.remove(user.group[0])
    db_sess.commit()
    db_sess.close()
