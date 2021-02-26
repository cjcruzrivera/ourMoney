from flask import Blueprint, render_template, redirect, url_for, request, flash
# from flask_login import login_required, current_user
# from .models import User, Calculo
from ..extensions import db
from ..models import User
# from datetime import datetime
# import json

main = Blueprint('main', __name__)

@main.route('/')
def index():
    users = User.query.all()
    return render_template('index.html', page_title="Dashboard", users=users, user={'nombre': "camilo"})
