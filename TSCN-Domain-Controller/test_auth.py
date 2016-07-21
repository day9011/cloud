# -*- coding:utf-8 -*-
__author__ = 'liming'

from flask import Flask, flash, redirect, url_for, request, get_flashed_messages
from flask.ext.login import LoginManager, UserMixin, current_user, login_user, logout_user

app = Flask(__name__)

# use for encrypt session
app.config['SECRET_KEY'] = 'SET T0 4NY SECRET KEY L1KE RAND0M H4SH'

login_manager = LoginManager()
login_manager.init_app(app)


class UserNotFoundError(Exception):
    pass


# Simple user class base on UserMixin
# http://flask-login.readthedocs.org/en/latest/_modules/flask/ext/login.html#UserMixin
class User(UserMixin):
    '''Simple User class'''
    USERS = {
        # username: password
        'liming': '123',
        'admin': '123'
    }

    def __init__(self, id):
        if not id in self.USERS:
            raise UserNotFoundError()
        self.id = id
        self.password = self.USERS[id]

    @classmethod
    def get(self_class, id):
        '''Return user instance of id, return None if not exist'''
        try:
            return self_class(id)
        except UserNotFoundError:
            return None


# Flask-Login use this to reload the user object from the user ID stored in the session
@login_manager.user_loader
def load_user(id):
    return User.get(id)


@app.route('/')
def index():
    # print current_user.is_authenticated()
    return (
        '''
            <h1>Hello {1}</h1>
            <p style="color: #f00;">{0}</p>
            <p>{2}</p>
        '''.format(
            # flash message
            ', '.join([ str(m) for m in get_flashed_messages() ]),
            current_user.get_id() or 'Guest',
            ('<a href="/logout">Logout</a>' if current_user.is_authenticated
                else '<a href="/login">Login</a>')
        )
    )
    # return 'hahaha this is index'


@app.route('/login')
def login():
    print app.config['SESSION_COOKIE_PATH']
    return '''
        <form action="/login/check" method="post">
            <p>Username: <input name="username" type="text"></p>
            <p>Password: <input name="password" type="password"></p>
            <input type="submit">
        </form>
    '''


@app.route('/login/check', methods=['post'])
def login_check():
    # validate username and password
    user = User.get(request.form['username'])
    if (user and user.password == request.form['password']):
        login_user(user)
    else:
        flash('Username or password incorrect')

    return redirect(url_for('index'))


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9996, debug = True)