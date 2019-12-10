from flaskps.extensions.db import db
from .school_year import SchoolYear
from .workshop import Workshop


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

    def __init__(self, student_id, cicle_id, workshop_id):
        self.student_id = student_id
        self.schoolyear_id = cicle_id
        self.workshop_id = workshop_id

    @classmethod
    def create(cls, student_id, cicle_id, workshop_id):
        cicle_id = cicle_id.split('-')[0] # Hasta que arreglen el problema
        course = cls(student_id, cicle_id, workshop_id)
        db.session.add(course)
        db.session.commit()

    @classmethod
    def get_students_doing_workshop(cls,schoolyear_id,workshop_id):
        students = cls.query.filter(cls.schoolyear_id==schoolyear_id,cls.workshop_id==workshop_id).all()
        students_ids = []
        for student in students:
            students_ids.append(student.student_id)
        return students_ids