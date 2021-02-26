import click
from flask.cli import with_appcontext

from .extensions import db
from .models import User, Cuenta, Transaccion

@click.command(name='create_tables')
@with_appcontext
def create_tables():
    db.drop_all()
    db.create_all()

    admin = User(
        email="cruz.camilo@correounivalle.edu.co",
        password="",
        username="admin",
        nombre="Administrador",
        apellidos="",
        img="",
        isAdmin=True
    )
    db.session.add(admin)
    db.session.commit()
