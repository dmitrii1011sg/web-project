import os

from data.user_model import User

PAGE_SIZE = 10

def created_diaposon(num_page, col_el, col_el_page):
    return col_el - (col_el_page * num_page), col_el - (col_el_page * (num_page - 1))

class DataBaseTool:
    def __init__(self, db_sess):
        self.db_sess = db_sess

    def create_user(self, login, password, phone_number: str, name, lastname, about, role) -> bool:
        print('create user', login, password, phone_number, name, lastname, about)
        user_login = self.db_sess.query(User).filter(User.login == login)
        if not user_login.first():
            user = User(login=login, phone_number=phone_number, name=name, lastname=lastname, about=about, role=role)
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

    def get_user_by_role(self, role, page=0):
        users = self.db_sess.query(User).filter(User.role == role).all()
        dia = created_diaposon(col_el=len(users), num_page=page, col_el_page=PAGE_SIZE)
        return users[dia[0]:dia[1]]
    