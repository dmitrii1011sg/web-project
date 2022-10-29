import os
from data.role_model import Role
from data.role_user_model import RoleUser

from data.user_model import User

class DataBaseTool:
    def __init__(self, db_sess):
        self.db_sess = db_sess

    def create_user(self, login, password, phone_number: str, name, lastname, about) -> bool:
        print('create user', login, password, phone_number, name, lastname, about)
        user_login = self.db_sess.query(User).filter(User.login == login)
        if not user_login.first():
            user = User(login=login, phone_number=phone_number, name=name, lastname=lastname, about=about)
            user.set_password(password)
            self.db_sess.add(user)
            self.db_sess.commit()
            print(f'Susseful add user: {login, name, lastname}')
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

    def get_user_by_role(self, role):
        users = self.db_sess.query(User).filter(User.role == role).all()
        return users
    