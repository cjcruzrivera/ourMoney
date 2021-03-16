""" Models for the app """
from flask_login import UserMixin
from sqlalchemy.ext.hybrid import hybrid_property

from .extensions import db


class User(UserMixin, db.Model):
    """ User class. Extends UserMixin for login purpose """
    __tablename__ = 'usuario'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100))
    password = db.Column(db.String(100))
    username = db.Column(db.String(100), unique=True)
    nombre = db.Column(db.String(100))
    apellidos = db.Column(db.String(100))
    img = db.Column(db.String(500))
    isAdmin = db.Column(db.Boolean, default=False)

    @hybrid_property
    def nombre_completo(self):
        """ Nombre Completo del Usuario """
        return "{} {}".format(self.nombre, self.apellidos)


class Cuenta(db.Model):
    """ Cuenta de dinero. Puede ser propia o ajena """
    __tablename__ = 'cuenta'

    tipos = {
        'propia': "Cuenta Propia",
        'ingreso': "Cuenta Externa de Ingreso",
        'egreso': "Cuenta Externa de Gasto",
        'deuda': "Cuenta de Deuda",
    }

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    tipo = db.Column(db.String(30))
    total = db.Column(db.Integer)

    @hybrid_property
    def saldo(self):
        """ total formated """
        self.total = self.total or 0
        return "${:,.0f}".format(self.total).replace(',', '.')

    def set_valor_origen(self, valor, reversed_trans=False):
        """ Set Value Cuenta Origen """
        if not reversed_trans:
            if self.tipo == "propia":
                self.total -= int(valor)

            if self.tipo == "deuda":
                self.total += int(valor)
        else:
            if self.tipo == "propia":
                self.total += int(valor)

            if self.tipo == "deuda":
                self.total -= int(valor)

    def set_valor_destino(self, valor, reversed_trans=False):
        """ Set Value Cuenta Origen """
        if not reversed_trans:
            if self.tipo == "propia":
                self.total += int(valor)

            if self.tipo == "deuda":
                self.total -= int(valor)
        else:
            if self.tipo == "propia":
                self.total -= int(valor)

            if self.tipo == "deuda":
                self.total += int(valor)


class Transaccion(db.Model):
    """ Transaccion de dinero """
    id = db.Column(db.Integer, primary_key=True)
    valor = db.Column(db.Integer)
    fecha_realiza = db.Column(db.DateTime)
    fecha_registra = db.Column(db.DateTime)

    realiza_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    registra_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    origen_id = db.Column(db.Integer, db.ForeignKey('cuenta.id'))
    destino_id = db.Column(db.Integer, db.ForeignKey('cuenta.id'))

    realiza = db.relationship(
        User, foreign_keys=realiza_id, backref="transacciones_realizadas")
    registra = db.relationship(
        User, foreign_keys=registra_id, backref="transacciones_registradas")
    origen = db.relationship(Cuenta, foreign_keys=origen_id, backref="egresos")
    destino = db.relationship(
        Cuenta, foreign_keys=destino_id, backref="ingresos")
