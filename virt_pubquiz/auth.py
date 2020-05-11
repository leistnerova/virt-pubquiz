from flask import Blueprint
from flask import (
    flash, render_template, request,
    redirect, url_for
)
from flask_login import login_required, login_user, logout_user
from werkzeug.security import check_password_hash

from .model import Users


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        user = Users.query.filter_by(name=request.form['name'].strip()).first()
        if not user or not check_password_hash(user.password, request.form['password']):
            flash('Wrong login name or password', 'danger')
            return redirect(url_for('auth.login'))
        login_user(user)
        return redirect(url_for('main.index'))
    else:
        return render_template('login.html')


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template('index.html')
