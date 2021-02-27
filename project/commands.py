import click
from flask.cli import with_appcontext
from getpass import getpass
from werkzeug.security import generate_password_hash

from .extensions import db
from .models import User, Cuenta, Transaccion


@click.command(name='create_tables')
@with_appcontext
def create_tables():
    db.drop_all()
    db.create_all()


@click.command(name='create_admin')
@with_appcontext
def create_admin():
    nombre = input("Nombre  (auto: Administrador): ")
    if nombre == "":
        nombre = "Administrador"

    username = input("Username (auto: admin): ")
    if username == "":
        username = "admin"

    password = generate_password_hash(getpass("Password: "))
    if password == "":
        print("Error. La contraseña no puede ser vacia")
        return False

    data = {
        'username': username,
        'email': "",
        'password': password,
        'nombre': nombre,
        'apellidos': "",
        'img': "",
        'isAdmin': True
    }
    admin = User(**data)
    db.session.add(admin)
    db.session.commit()
