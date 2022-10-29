import os

from data.user_model import User

class DataBaseTool:
    def __init__(self, db_sess):
        self.db_sess = db_sess

    def create_user(self, login, password, roles, phone_number: str) -> bool:
        user_login = self.db_sess.query(User).filter(User.login == login)
        if not user_login.first():
            user = User(login=login, roles=roles, phone_number=phone_number)
            user.set_password(password)
            self.db_sess.add(user)
            self.db_sess.commit()
            print(f'Susseful add user: {login, roles}')
            return True
        return False

    def check_user(self, login, password):
        user = self.db_sess.query(User).filter(User.login == login).first()
        if user and user.check_password(password):
            return user
        return False

    