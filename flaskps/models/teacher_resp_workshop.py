from flaskps.extensions.db import db
from .school_year import SchoolYear
from .workshop import Workshop


school_year_workshop_teacher = db.Table(
    'docente_responsable_taller',
    db.Column(
        'docente_id',
        db.Integer,
        db.ForeignKey('docente.id'),
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
