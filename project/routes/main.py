from flask import Blueprint, render_template, redirect, request, flash, url_for
from flask_login import login_required#, current_user

from ..models import Cuenta
from ..extensions import db
# from .models import User, Calculo
# from ..models import User
# from datetime import datetime
# import json

main = Blueprint('main', __name__)

@main.route('/')
@login_required
def index():
    """ Dashboard """
    return render_template('index.html')

'''""" Modulo de Cuentas """'''

@main.route('/cuentas/crear', methods=['POST', 'GET'])
@login_required
def crear_cuenta():
    """ Crear cuentas C"""
    if request.method == "GET":
        return render_template('cuentas/crear_cuenta.html')

    nombre = request.form.get("nombre")

    cuenta = Cuenta.query.filter_by(nombre=nombre).first()
    if cuenta:
        flash('Ya existe una cuenta con ese nombre' , 'danger')
        return redirect(url_for('main.crear_cuenta'))

    # TODO: Validar Saldo como dato obligatorio en caso de cuenta propia
    tipo = request.form.get("tipo")
    total = request.form.get("total")

    cuenta = Cuenta(nombre=nombre, tipo=tipo, total=total)
    db.session.add(cuenta)
    db.session.commit()
    flash("Cuenta '{}' creada correctamente".format(nombre), 'success')
    return redirect(url_for('main.cuentas'))


@main.route('/cuentas')
@login_required
def cuentas():
    """ Index cuentas. R """
    cuentas_reg = Cuenta.query.order_by(Cuenta.id).all()
    return render_template('cuentas/cuentas.html', cuentas=cuentas_reg)

@main.route('/cuentas/editar/<cuenta_id>', methods=['GET', 'POST'])
@login_required
def editar_cuenta(cuenta_id):
    """ Editar una cuenta. U """
    cuenta = Cuenta.query.filter_by(id=cuenta_id).first_or_404(description="No se encuentra ninguna cuenta registrada con id {}".format(cuenta_id))
    if request.method == "GET":
        return render_template("cuentas/editar_cuenta.html", cuenta=cuenta)

    nombre = request.form.get("nombre")

    cuenta_valid = Cuenta.query.filter_by(nombre=nombre).first()
    if cuenta_valid and cuenta.id != cuenta_valid.id:
        flash('Ya existe una cuenta con ese nombre' , 'danger')
        return redirect(url_for('main.editar_cuenta', ))

    # TODO: Validar Saldo como dato obligatorio en caso de cuenta propia
    tipo = request.form.get("tipo")
    total = request.form.get("total")
    cuenta.nombre = nombre
    cuenta.tipo = tipo
    cuenta.total = total
    # TODO: El total no deberia poderse editar
    db.session.add(cuenta)
    db.session.commit()
    flash("Cuenta '{}' editada correctamente".format(nombre), 'success')
    return redirect(url_for('main.cuentas'))


# TODO: El crear y editar debe quedar en un modal

@main.route('/cuentas/eliminar/<cuenta_id>')
@login_required
def eliminar_cuenta(cuenta_id):
    """ Eliminar una cuenta. D """
    cuenta = Cuenta.query.filter_by(id=cuenta_id).first_or_404(description="No se encuentra ninguna cuenta registrada con id {}".format(cuenta_id))
    db.session.delete(cuenta)
    db.session.commit()
    flash('Cuenta con id "{}" eliminada correctamente'.format(cuenta_id), 'warning')
    return redirect(url_for('main.cuentas'))

'''""" Modulo de Movimientos """'''

@main.route('/movimientos')
@login_required
def movimientos():
    return render_template('movimientos.html')


'''""" Modulo de Reportes """'''

@main.route('/reportes')
@login_required
def reportes():
    return render_template('reportes.html')

'''""" Modulo de Administrador """'''

@main.route('/admin')
@login_required
def admin():
    return render_template('admin.html')


'''""" Modulo de Errores. TODO:Arreglar Handler """'''

@main.errorhandler(404)
def page_not_found(error):
    """ View for 404 error handling """
    return render_template("error.html", error=error), 404
