from flaskps.extensions.db import db
from .school_year import SchoolYear
from .workshop import Workshop

school_year_workshop = db.Table(
    'ciclo_lectivo_taller',
    db.Column(
        'taller_id',
        db.Integer,
        db.ForeignKey('workshop.id'),
        primary_key=True
    ),
    db.Column(
        'ciclo_lectivo_id',
        db.Integer,
        db.ForeignKey('schoolYear.id'),
        primary_key=True
    )
)
