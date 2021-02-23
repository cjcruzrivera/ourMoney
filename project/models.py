""" Models for the app """
from flask_login import UserMixin
from .extensions import db

class User(UserMixin, db.Model):
    """ User class. Extends UserMixin for login purpose """
    __tablename__ = 'usuario'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    username = db.Column(db.String(100))
    nombre = db.Column(db.String(100))
    apellidos = db.Column(db.String(100))
    img = db.Column(db.String(500))
    isAdmin = db.Column(db.Boolean, default=False)


class Fuente(db.Model):
    """ Fuente de dinero. Puede ser propia o ajena """
    __tablename__ = 'fuente'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    tipo = db.Column(db.String(10)) #propia, externa, deuda
    total = db.Column(db.Integer)


class Transaccion(db.Model):
    """ Transaccion de dinero """
    id = db.Column(db.Integer, primary_key=True)
    valor = db.Column(db.Integer)
    fecha = db.Column(db.DateTime)

    quien_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    registra_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    origen_id = db.Column(db.Integer, db.ForeignKey('fuente.id'))
    destino_id = db.Column(db.Integer, db.ForeignKey('fuente.id'))

    quien = db.relationship(User, foreign_keys=quien_id, backref="transacciones_realizadas")
    registra = db.relationship(User, foreign_keys=registra_id, backref="transacciones_registradas")
    origen = db.relationship(Fuente, foreign_keys=origen_id, backref="egresos")
    destino = db.relationship(Fuente, foreign_keys=destino_id, backref="ingresos")