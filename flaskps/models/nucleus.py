from flaskps.extensions.db import db


class Nucleus(db.Model):
    __tablename__ = 'nucleo'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        'nombre',
        db.String(255),
        nullable=False
    )

    address = db.Column(
        'direccion',
        db.String(255),
        nullable=True
    )

    telephone = db.Column(
        'telefono',
        db.String(255),
        nullable=True
    )
