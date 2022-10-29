import sqlalchemy
from .db_session import SqlAlchemyBase


class Friend(SqlAlchemyBase):
    __tablename__ = 'friends'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    first_user_id = sqlalchemy.Column(sqlalchemy.Integer)
    second_user_id = sqlalchemy.Column(sqlalchemy.Integer)
