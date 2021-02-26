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
    return render_template('index.html', user={'nombre': "camilo"})

@main.route('/cuentas')
def cuentas():
    return render_template('cuentas.html', user={'nombre': "camilo"})

@main.route('/movimientos')
def movimientos():
    return render_template('movimientos.html', user={'nombre': "camilo"})

@main.route('/reportes')
def reportes():
    return render_template('reportes.html', user={'nombre': "camilo"})

@main.route('/admin')
def admin():
    return render_template('admin.html', user={'nombre': "camilo"})