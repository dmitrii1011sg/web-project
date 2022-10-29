from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField


class RegisterForm(FlaskForm):
    login = StringField('Login', validators=[DataRequired()])
    phone_number = StringField('Phone number', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    lastname = StringField('Last Name')
    about = TextAreaField('About')
    password = PasswordField('Password', validators=[DataRequired()])
    password_again = PasswordField('Repeat password', validators=[DataRequired()])
    role = StringField('Role')
    submit = SubmitField('Register')