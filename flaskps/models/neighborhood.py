from flaskps.extensions.db import db


class Neighborhood(db.Model):
    __tablename__ = 'barrio'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        'nombre',
        db.String(255),
        nullable=False
    )

    students = db.relationship('Student', backref='barrio', lazy=True)
