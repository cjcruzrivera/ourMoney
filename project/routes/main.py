from flask import Blueprint, render_template, redirect, request, flash, url_for
from flask_login import login_required, current_user
from datetime import datetime

from ..models import Cuenta, Transaccion, User
from ..extensions import db
# from .models import User, Calculo
# from ..models import User
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
        return render_template('cuentas/crear_cuenta.html', tipos = Cuenta.tipos)

    nombre = request.form.get("nombre")

    cuenta = Cuenta.query.filter_by(nombre=nombre).first()
    if cuenta:
        flash('Ya existe una cuenta con ese nombre', 'danger')
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
    cuenta = Cuenta.query.filter_by(id=cuenta_id).first_or_404(
        description="No se encuentra ninguna cuenta registrada con id {}".format(cuenta_id))
    if request.method == "GET":
        return render_template("cuentas/editar_cuenta.html", cuenta=cuenta, tipos = Cuenta.tipos)

    nombre = request.form.get("nombre")

    cuenta_valid = Cuenta.query.filter_by(nombre=nombre).first()
    if cuenta_valid and cuenta.id != cuenta_valid.id:
        flash('Ya existe una cuenta con ese nombre', 'danger')
        return redirect(url_for('main.editar_cuenta', ))

    # TODO: Validar Saldo como dato obligatorio en caso de cuenta propia
    tipo = request.form.get("tipo")
    total = request.form.get("total")
    cuenta.nombre = nombre
    cuenta.tipo = tipo
    cuenta.total = total

    db.session.add(cuenta)
    db.session.commit()
    flash("Cuenta '{}' editada correctamente".format(nombre), 'success')
    return redirect(url_for('main.cuentas'))


#TODO: El crear y editar debe quedar en un modal

@main.route('/cuentas/eliminar/<cuenta_id>')
@login_required
def eliminar_cuenta(cuenta_id):
    """ Eliminar una cuenta. D """
    cuenta = Cuenta.query.filter_by(id=cuenta_id).first_or_404(
        description="No se encuentra ninguna cuenta registrada con id {}".format(cuenta_id))
    db.session.delete(cuenta)
    db.session.commit()
    flash('Cuenta con id "{}" eliminada correctamente'.format(cuenta_id), 'warning')
    return redirect(url_for('main.cuentas'))


'''""" Modulo de transacciones """'''


@main.route('/transacciones/crear', methods=['GET', 'POST'])
@login_required
def crear_transaccion():
    """ Crear transaccion. C"""
    if request.method == "GET":
        usuarios = User.query.all()
        cuentas_reg = Cuenta.query.all()
        return render_template('transacciones/crear_transaccion.html', usuarios=usuarios, cuentas=cuentas_reg)

    origen_id = request.form.get("origen")
    destino_id = request.form.get("destino")
    realiza_id = request.form.get("realiza")
    valor = request.form.get("total")
    fecha_realiza_str = request.form.get("fecha_realiza")
    fecha_realiza = datetime.strptime(fecha_realiza_str, '%m/%d/%Y %H:%M %p')

    origen = Cuenta.query.filter_by(id=origen_id).first()
    destino = Cuenta.query.filter_by(id=destino_id).first()
    realiza = User.query.filter_by(id=realiza_id).first()

    origen.set_valor_origen(valor, reversed_trans=False)
    destino.set_valor_destino(valor, reversed_trans=False)
    

    transaccion = Transaccion(valor=valor, origen=origen, destino=destino, registra=current_user,
                              realiza=realiza, fecha_realiza=fecha_realiza, fecha_registra=datetime.today())

    objects = [origen, destino]
    db.session.bulk_save_objects(objects)
    db.session.add(transaccion)
    db.session.commit()
    flash("Transaccion registrada correctamente", 'success')
    return redirect(url_for('main.transacciones'))


@main.route('/transacciones')
@login_required
def transacciones():
    """ Lista de transacciones. R"""
    transacciones_registradas = Transaccion.query.all()
    return render_template('transacciones/transacciones.html', transacciones=transacciones_registradas)


@main.route('/transacciones/editar/<transaccion_id>', methods=['GET', 'POST'])
@login_required
def editar_transaccion(transaccion_id):
    """ Editar una transaccion. U """
    transaccion = Transaccion.query.filter_by(id=transaccion_id).first_or_404(
        description="No se encuentra ninguna transaccion registrada con id {}".format(transaccion_id))
    usuarios = User.query.all()
    cuentas_reg = Cuenta.query.all()
    if request.method == "GET":
        return render_template('transacciones/editar_transaccion.html', transaccion=transaccion, usuarios=usuarios, cuentas=cuentas_reg)
    
    #Se reversa la transaccion original
    origen_old = transaccion.origen
    destino_old = transaccion.destino
    origen_old.set_valor_origen(transaccion.valor, reversed_trans=True)
    destino_old.set_valor_destino(transaccion.valor, reversed_trans=True)

    db.session.bulk_save_objects([origen_old, destino_old])
    db.session.commit()

    #Se crea la nueva transaccion
    origen_id = request.form.get("origen")
    destino_id = request.form.get("destino")
    realiza_id = request.form.get("realiza")
    valor = request.form.get("total")
    fecha_realiza_str = request.form.get("fecha_realiza")
    fecha_realiza = datetime.strptime(fecha_realiza_str, '%m/%d/%Y %H:%M %p')

    origen = Cuenta.query.filter_by(id=origen_id).first()
    destino = Cuenta.query.filter_by(id=destino_id).first()
    realiza = User.query.filter_by(id=realiza_id).first()

    origen.set_valor_origen(valor, reversed_trans=False)
    destino.set_valor_destino(valor, reversed_trans=False)

    transaccion.origen = origen
    transaccion.destino = destino
    transaccion.valor = valor
    transaccion.realiza = realiza
    transaccion.fecha_realiza = fecha_realiza

    db.session.bulk_save_objects([origen, destino])
    db.session.add(transaccion)
    db.session.commit()
    flash("Transaccion editada correctamente", 'success')
    return redirect(url_for('main.transacciones'))

@main.route('/transacciones/eliminar/<transaccion_id>', methods=['GET', 'POST'])
@login_required
def eliminar_transaccion(transaccion_id):
    """ eliminar una transaccion. D """
    transaccion = Transaccion.query.filter_by(id=transaccion_id).first_or_404(
        description="No se encuentra ninguna transaccion registrada con id {}".format(transaccion_id))

    origen = transaccion.origen#Cuenta.query.filter_by(id=transaccion.origen_id).first()
    destino = transaccion.destino#Cuenta.query.filter_by(id=transaccion.destino_id).first()

    origen.set_valor_origen(transaccion.valor, reversed_trans=True)
    destino.set_valor_destino(transaccion.valor, reversed_trans=True)

    objects = [origen, destino]
    db.session.bulk_save_objects(objects)
    db.session.delete(transaccion)
    db.session.commit()
    flash('Transaccion con id "{}" eliminada correctamente'.format(
        transaccion_id), 'warning')
    return redirect(url_for('main.transacciones'))


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
