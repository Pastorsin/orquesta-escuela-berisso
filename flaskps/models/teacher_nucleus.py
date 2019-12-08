from flaskps.extensions.db import db
from .school_year import SchoolYear
from .workshop import Workshop

teacher_nucleus = db.Table(
    'docente_nucleo',
    db.Column(
        'docente_id',
        db.Integer,
        db.ForeignKey('docente.id'),
        primary_key=True
    ),
    db.Column(
        'nucleo_id',
        db.Integer,
        db.ForeignKey('nucleo.id'),
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
    ),
    db.Column(
        'dia',
        db.Integer,
        db.ForeignKey('dia.id'),
        primary_key=True
        ),
    db.ForeignKeyConstraint(
        ['taller_id', 'ciclo_lectivo_id'],
        ['ciclo_lectivo_taller.taller_id', 'ciclo_lectivo_taller.ciclo_lectivo_id']
        )
)
