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
    avatar = sqlalchemy.Column(sqlalchemy.Text, default='data:image/jpeg;base64,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3lZb9acQUbCcJfSm5XZap3piT8cPNMsMkS5HMhP1f//aAAwDAQACAAMAAAAQ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++35y++++++++++++6G//uf+++++++++++8//wD/AO/37777777777z/AP8A/wD+v7777777777X/wD/AP8A/wA++++++++++1//AP8A/wD8++++++++++7/AP8A/wD/APPvvvvvvvvvvqsNcFHvvvvvvvvvvvvutdvvvvvvvvvvvvpP/wD/APt9+++++++++3//AP8A/wD/AP8A77777777x/8A/wD/AP8A/wD7vfvvvvvvf/8A/wD/AP8A/wD/AHPvvvvrn/8A/wD/AP8A/wD/AP6vvvv/xAAeEQEAAgICAwEAAAAAAAAAAAABETAAIDFBIUBRUP/aAAgBAwEBPxD9pQyGCN3w06GxQbKSvn6Pltzr5bc6z3sIsfnJ5LJ4QukyGSWsMVdBGEqugok8NCgqUm6lqfnZv//EABwRAQADAQEBAQEAAAAAAAAAAAEAETAgMUAhUP/aAAgBAgEBPxD+1UplbBwmg6SvsDzrxmedeM10tCKSkpHZUplahcCuEGJWQYJgF5JXYfmQ+X//xAAqEAEAAQEGBgEFAQEAAAAAAAABEQAhMUBBUWEwcYGRocHRILHh8PFQcP/aAAgBAQABPxD/AL5rdwK15F7TaI6wB72+Kt8vepTbBrJRkk9ZzuTWy+E4sKayiAKk1uVnYZG9/KmhpKkr1+kmKZsf2pZFYFib6PjliVAVYCkZjZZzN2078GcWtjPP120xDxEbIvzO93fhISIMiXjU5S5dmfUtw7gM9iWHz14bu8doWns64ZwWAk0bB5eJcmd5jNM7IgdnCxo2meQL9w4spsof2csLBrEdPy4v7QTPvCuwyH8nFUnoGFIMqh2flxZVqvA9YVDyZVsD8HFQKQpdSniMK5SehVp5KRGGx4YiWc7TnQ8QQtggw18XUc+/o38OybhMWiv6stueHIecBIlS93kntannnV6ggYTp9ZR4ymjnpULxtG0O7PldzxWi9I2OVOqo6nuaS2JzPRTk9l80SWryHzT3b0eqZGxZv4XeKEBVwh2P95tC14gdC2n3t194obaeYPdObNySiIKbnqaiJ/Qz2vxV5Q5YKdkXL6L3eKUZ7neAs+oYZL6ZAlsfNp0aSRezO9bz9toMjSJImGjncUPdevtSzJAuNgZcM2zDNpXw7lWrQJZabmpvhFVkLSu2+VKqqyufFX0cohGh6Acg6m+36YFhGohFzRvrgGxOkIR1qZ4DZujo94AVQZ1ZOfR8U5ZUqsq4Gd0pNHUdmnbsbc2YPGZkBKuRUhnoYfN/XBtYBIJuyXrd241zBXlP8HXCICIGRMqJpJQNBY/PXiy0kTnX+THTCyvsIO5Y+u3Evha+QTSsSxt1nC28whyPycRL9PlHthmcQkjVlkRQ5n1f/9k=')
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    role = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    phone_number = sqlalchemy.Column(sqlalchemy.String)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)

    def set_password(self, password: str):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password: str) -> boolean:
        return check_password_hash(self.hashed_password, password)

    def get_user_information(self) -> dict:
        information = {
            'id': self.id,
            'login': self.login,
            'name': self.name,
            'lastname': self.lastname,
            'about': self.about,
            'phone_number': self.phone_number,
            'create_date': self.created_date,
            'avatar': self.avatar
        }
        return information