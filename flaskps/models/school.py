from flaskps.extensions.db import db


class School(db.Model):
    __tablename__ = 'escuela'

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

    students = db.relationship('Student', backref='school', lazy=True)
