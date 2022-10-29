import datetime
from email.policy import default
from multiprocessing.util import info
from xmlrpc.client import boolean
import sqlalchemy
from flask_login import UserMixin
from .db_session import SqlAlchemyBase
from werkzeug.security import generate_password_hash, check_password_hash


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    login = sqlalchemy.Column(sqlalchemy.String, index=True, unique=True)
    name = sqlalchemy.Column(sqlalchemy.String, index=True)
    lastname = sqlalchemy.Column(sqlalchemy.String, index=True, nullable=True)
    about = sqlalchemy.Column(sqlalchemy.String, index=True, nullable=True, default='Nothing')
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    roles = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    phone_number = sqlalchemy.Column(sqlalchemy.String)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)

    def set_password(self, password: str):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password: str) -> boolean:
        return check_password_hash(self.hashed_password, password)

    def get_user_information(self) -> dict:
        information = {
            'login': self.login,
            'name': self.name,
            'lastname': self.lastname,
            'about': self.about,
            'phone_number': self.phone_number,
            'create_date': self.created_date
        }
        return information