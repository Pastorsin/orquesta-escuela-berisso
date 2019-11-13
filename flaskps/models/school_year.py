from flaskps.extensions.db import db


class SchoolYear(db.Model):
    __tablename__ = 'ciclo_lectivo'

    start_date = db.Column(
        'fecha_inicio',
        db.DateTime,
        nullable=False
    )

    finish_date = db.Column(
        'fecha_fin',
        db.DateTime,
        nullable=False
    )

    semester = db.Column(
        'semestre',
        db.Integer,
        nullable=False
    )
