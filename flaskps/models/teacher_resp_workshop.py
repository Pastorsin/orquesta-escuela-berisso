from flaskps.extensions.db import db
from .school_year import SchoolYear
from .workshop import Workshop
from .teacher import Teacher

school_year_workshop = db.Table(
    'docente_responsable_taller',
    db.Column(
        'docente_id',
        db.Integer,
        db.ForeignKey('teacher.id'),
        primary_key=True
    ),
    db.Column(
        'ciclo_lectivo_id',
        db.Integer,
        db.ForeignKey('schoolYear.id'),
        primary_key=True
    ),
    db.Column(
        'taller_id',
        db.Integer,
        db.ForeignKey('workshop.id'),
        primary_key=True
    )
)
