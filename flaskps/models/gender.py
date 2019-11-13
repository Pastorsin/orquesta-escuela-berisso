from flaskps.extensions.db import db


class Gender(db.Model):
    __tablename__ = 'genero'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        'nombre',
        db.String(255),
        nullable=False
    )

    students = db.relationship('Student', backref='gender', lazy=True)
