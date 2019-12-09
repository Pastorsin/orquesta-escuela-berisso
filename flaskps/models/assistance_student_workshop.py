from flaskps.extensions.db import db

from flaskps.extensions.db import db


class AssistanceStudentWorkshop(db.Model):
    __tablename__ = 'asistencia_estudiante_taller'

    student_id = db.Column(
        'estudiante_id',
        db.Integer,
        db.ForeignKey('estudiante.id'),
        primary_key=True
    ),
    schoolyear_id = db.Column(
        'ciclo_lectivo_id',
        db.Integer,
        db.ForeignKey('ciclo_lectivo.id'),
        primary_key=True
    ),
    workshop_id = db.Column(
        'taller_id',
        db.Integer,
        db.ForeignKey('taller.id'),
        primary_key=True
    ),
    date = db.Column(
        'fecha',
        db.Date,
        primary_key=True
    )

    __table_args__ = (
        db.ForeignKeyConstraint(
            ['taller_id', 'ciclo_lectivo_id'],
            ['ciclo_lectivo_taller.taller_id',
                'ciclo_lectivo_taller.ciclo_lectivo_id']
        ),
        db.ForeignKeyConstraint(
            'estudiante_id','estudiante.id'
        )
    )
