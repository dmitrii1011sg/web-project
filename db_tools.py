from sqlalchemy import or_
import os
from data.friends_model import Friend

from data.user_model import User

PAGE_SIZE = 10

def created_diaposon(num_page, col_el, col_el_page):
    return col_el - (col_el_page * num_page), col_el - (col_el_page * (num_page - 1))

class DataBaseTool:
    def __init__(self, db_sess):
        self.db_sess = db_sess

    def create_user(self, login, password, phone_number: str, name, lastname, about, role) -> bool:
        user_login = self.db_sess.query(User).filter(User.login == login)
        if not user_login.first():
            user = User(login=login, phone_number=phone_number, name=name, lastname=lastname, about=about, role=role)
            user.set_password(password)
            self.db_sess.add(user)
            self.db_sess.commit()
            return True
        return False

    def check_user(self, login, password):
        user = self.db_sess.query(User).filter(User.login == login).first()
        if user and user.check_password(password):
            return user
        return False

    def get_user_info_by_id(self, id: int):
        user = self.db_sess.query(User).filter(User.id == id).first() 
        if user: return user.get_user_information()
        return False

    def get_user_by_role(self, role, page=0):
        users = self.db_sess.query(User).filter(User.role == role).all()
        dia = created_diaposon(col_el=len(users), num_page=page, col_el_page=PAGE_SIZE)
        return users[dia[0]:dia[1]]

    def add_friends(self, current_user_id, user_id):
        current_user = self.db_sess.query(User).filter(User.id == current_user_id).first()
        user = self.db_sess.query(User).filter(User.id == user_id).first()
        if user and current_user:
            friends = Friend(first_user_id=current_user_id, second_user_id=user_id)
            self.db_sess.add(friends)
            self.db_sess.commit()
            return True
        return False

    def get_friends_by_user_id(self, user_id, page):
        user = self.db_sess.query(User).filter(User.id == user_id).first()
        if user:
            friends = self.db_sess.query(Friend).filter(
                or_(Friend.first_user_id == user_id, Friend.second_user_id == user_id)).all()
            ids = map(lambda f: f.first_user_id if f.first_user_id != user_id else f.second_user_id, friends)
            users = self.db_sess.query(User).filter(User.id.in_(ids)).all()
            dia = created_diaposon(col_el=len(users), num_page=page, col_el_page=PAGE_SIZE)
            return users[dia[0]:dia[1]]

    def check_friend(self, current_user_id, user_id):
        friend = self.db_sess.query(Friend).filter(
            or_(
                Friend.first_user_id == current_user_id, Friend.second_user_id == user_id,
                Friend.first_user_id == user_id, Friend.second_user_id == current_user_id
            )
        ).first()
        return True if friend else False

    def delete_friend(self, current_user_id, user_id):
        self.db_sess.query(Friend).filter(
            or_(
                Friend.first_user_id == current_user_id, Friend.second_user_id == user_id,
                Friend.first_user_id == user_id, Friend.second_user_id == current_user_id
            )
        ).delete()
        self.db_sess.commit()
