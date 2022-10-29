from os import getenv
from unicodedata import name
from dotenv import load_dotenv
import flask_login
from flask import Flask, render_template, redirect, request
from flask_login import LoginManager, login_required, logout_user, current_user
from data import db_session
from data.user_model import User
from flask_form.login_form import LoginUserForm
from flask_form.register_form import RegisterForm
from db_tools import DataBaseTool

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = getenv('TOKEN')
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('main.template.html', context={'title_page': 'Main'})

@app.route('/login', methods=['GET', 'POST'])
def login_user():
    context = {'title_page': 'Login'}
    data_tool = DataBaseTool(db_session.create_session())
    form = LoginUserForm()
    context['form'] = form
    if form.validate_on_submit():
        user = data_tool.check_user(login=form.login.data,
                                    password=form.password.data)
        if user:
            flask_login.login_user(user, remember=form.remember_me.data)
            return redirect("/")
        context['message'] = 'incorrect'
        return render_template('login.template.html', context=context)
    return render_template('login.template.html', context=context)

@app.route('/register', methods=['GET', 'POST'])
def regist_user():
    data_tool = DataBaseTool(db_session.create_session())  
    context = {'title_page': 'Sing Up'}

    form = RegisterForm()  
    context['form'] = form
    print(form.data)
    if form.validate_on_submit():  
        print('validate success')
        if form.password.data != form.password_again.data:  
            context['message'] = 'Passwords do not match'
            return render_template('register.template.html', context=context)
        user_info = data_tool.create_user(login=form.login.data,
                                            password=form.password.data,
                                            phone_number=form.phone_number.data,
                                            name=form.name.data,
                                            lastname=form.lastname.data,
                                            about=form.about.data,
                                            role=form.role.data)

        if user_info:
            return redirect("/login")
        else:
            context['message'] = f'User with login {form.login.data} already exists'
            return render_template('register.template.html', context=context)
    return render_template('register.template.html', context=context)

@app.route('/profile/<int:id>')
def profile_user(id: int):
    data_tool = DataBaseTool(db_session.create_session())  
    context = {'title_page': 'Profile', 'user': data_tool.get_user_info_by_id(id), 'friend': data_tool.check_friend(current_user_id=current_user.id, user_id=id)}
    return render_template('profile-user.template.html', context=context)
    
@app.route('/users')
def users_list():
    data_tool = DataBaseTool(db_session.create_session())  
    page_number = request.args.get('page')
    if current_user.is_authenticated:
        role = current_user.role
        context = {'title_page': 'Users', 'users': data_tool.get_user_by_role(role, int(page_number)), 'page': int(page_number)}
        return render_template('users-list.template.html', context=context)
    return redirect('/')

@app.route('/friends')
def frinends_list():
    data_tool = DataBaseTool(db_session.create_session())  
    page_number = request.args.get('page')
    if current_user.is_authenticated:
        context = {'title_page': 'Friends', 'users': data_tool.get_friends_by_user_id(current_user.id, int(page_number)), 'page': int(page_number)}
        return render_template('users-list.template.html', context=context)
    return redirect('/')

@app.route('/add_friend/', methods=['POST'])
def add_friend():
    index = request.form['index']
    print(index)
    data_tool = DataBaseTool(db_session.create_session()) 
    data_tool.add_friends(current_user_id=int(current_user.id), user_id=int(index)) 
    return redirect('/')

@app.route('/delete_friend/', methods=['POST'])
def delete_friend():
    index = request.form['index']
    print(index)
    data_tool = DataBaseTool(db_session.create_session()) 
    data_tool.delete_friend(current_user_id=current_user.id, user_id=index) 
    return redirect('/')


    

def main():
    db_session.global_init("db/database.db")
    app.run(debug=True)

if __name__ == '__main__':
    main()