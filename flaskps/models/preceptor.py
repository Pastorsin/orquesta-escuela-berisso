from flaskps.extensions.db import db


class Preceptor(db.Model):
    __tablename__ = 'preceptor'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    last_name = db.Column(
        'apellido',
        db.String(30),
        nullable=False
    )

    first_name = db.Column(
        'nombre',
        db.String(20),
        nullable=False
    )

    telephone = db.Column(
        'tel',
        db.String(255),
        nullable=False
    )
