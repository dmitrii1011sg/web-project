from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField


class RegisterForm(FlaskForm):
    login = StringField('Login', validators=[DataRequired()])
    phone_number = StringField('Phone number', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password_again = PasswordField('Repeat password', validators=[DataRequired()])
    roles = StringField('Roles')
    submit = SubmitField('Register')