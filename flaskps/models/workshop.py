from flaskps.extensions.db import db
from .school_year_workshop import school_year_workshop


class Workshop(db.Model):
    __tablename__ = 'taller'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        'nombre',
        db.String(255),
        nullable=False
    )

    short_name = db.Column(
        'nombre_corto',
        db.String(255),
        nullable=False
    )
