from flaskps.extensions.db import db


class StudentWorkshop(db.Model):
    __tablename__ = 'estudiante_taller'

    student_id = db.Column(
        'estudiante_id',
        db.Integer,
        db.ForeignKey('estudiante.id'),
        primary_key=True
    )

    schoolyear_id = db.Column(
        'ciclo_lectivo_id',
        db.Integer,
        db.ForeignKey('ciclo_lectivo.id'),
        primary_key=True
    )

    workshop_id = db.Column(
        'taller_id',
        db.Integer,
        db.ForeignKey('taller.id'),
        primary_key=True
    )

    __table_args__ = (
        db.ForeignKeyConstraint(
            ['taller_id', 'ciclo_lectivo_id'],
            ['ciclo_lectivo_taller.taller_id',
                'ciclo_lectivo_taller.ciclo_lectivo_id']
        ),
    )

    @classmethod
    def get_students(cls):
        return students
