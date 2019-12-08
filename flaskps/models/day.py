from flaskps.extensions.db import db


class Day(db.Model):
    __tablename__ = 'dia'

    id = db.Column(
        db.Integer,
        primary_key=True
    ),

    name = db.Column(
        'nombre',
        db.String(15),
        nullable=False
    )

