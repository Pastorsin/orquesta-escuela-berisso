from flaskps.extensions.db import db


class Level(db.Model):
    __tablename__ = 'nivel'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        'nombre',
        db.String(255),
        nullable=False
    )

    students = db.relationship('Student', backref='nivel', lazy=True)
