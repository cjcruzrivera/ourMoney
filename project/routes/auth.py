from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user, login_required
from ..models import User
from ..extensions import db

auth = Blueprint('auth', __name__)


@auth.route('/login')
def login():
    next_page = ""
    param = request.args.get('next')

    if param is not None:
        next_page = param

    return render_template('login.html', next_page=next_page)

@auth.route('/login', methods=['POST'])
def login_post():
    username = request.form.get('username')
    password = request.form.get('password')
    req_next_page = request.form.get('next_page', "")

    if req_next_page == "":
        next_page = url_for("main.index")
    else:
        next_page = req_next_page
    
    user = User.query.filter_by(username=username).first()

    # check if the user actually exists TODO: Cambiar validacion para mensaje concreto
    if not user or not check_password_hash(user.password, password):
        flash('Nombre de Usuario o contraseña incorrectos', 'danger')
        return redirect(url_for('auth.login'))

    login_user(user)
    return redirect(next_page)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
