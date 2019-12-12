from flaskps.extensions.db import db


class Day(db.Model):
    __tablename__ = 'dia'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        'nombre',
        db.String(15),
        unique=True,
        nullable=False
    )

    number = db.Column(
        'numero',
        db.Integer,
        unique=True,
        nullable=False
    )

    teacher_nucleus = db.relationship(
        'TeacherNucleus',
        backref='day',
        lazy=True
    )
