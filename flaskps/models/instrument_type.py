from flaskps.extensions.db import db


class InstrumentType(db.Model):
    __tablename__ = 'tipo_instrumento'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        'nombre',
        db.String(255),
        nullable=False
    )
