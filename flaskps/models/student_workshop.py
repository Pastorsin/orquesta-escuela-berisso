from flaskps.extensions.db import db
from .school_year import SchoolYear
from .workshop import Workshop


school_year_workshop_student = db.Table(
    'estudiante_taller',
    db.Column(
        'estudiante_id',
        db.Integer,
        db.ForeignKey('estudiante.id'),
        primary_key=True
    ),
    db.Column(
        'ciclo_lectivo_id',
        db.Integer,
        db.ForeignKey('ciclo_lectivo.id'),
        primary_key=True
    ),
    db.Column(
        'taller_id',
        db.Integer,
        db.ForeignKey('taller.id'),
        primary_key=True
    )
)
