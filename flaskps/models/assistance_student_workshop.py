from flaskps.extensions.db import db
from datetime import datetime


class AssistanceStudentWorkshop(db.Model):
    __tablename__ = 'asistencia_estudiante_taller'

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

    nucleus_id = db.Column(
        'nucleo_id',
        db.Integer,
        db.ForeignKey('nucleo.id'),
        primary_key=True
    )

    date = db.Column(
        'fecha',
        db.Date,
        primary_key=True
    )

    assisted = db.Column(
        'asistio',
        db.Integer,
    )

    observation = db.Column(
        'observacion',
        db.String(255),
        nullable=True,
    )

    __table_args__ = (
        db.ForeignKeyConstraint(
            ['taller_id', 'ciclo_lectivo_id'],
            ['ciclo_lectivo_taller.taller_id',
                'ciclo_lectivo_taller.ciclo_lectivo_id']
        ),
    )

    def __init__(self, data):
        self.__init_attributes(data)

    def __init_attributes(self, data):
        self.student_id = data['student_id']
        self.schoolyear_id = data['schoolyear_id']
        self.workshop_id = data['workshop_id']
        self.nucleus_id = data['nucleus_id']
        self.date = data['date']
        self.assisted = data['assistance']
        self.observation = data['observation']

    @classmethod
    def create(cls, data):
        assistance_student_workshop = cls(data)
        db.session.add(assistance_student_workshop)
        db.session.commit()

    @classmethod
    def assistance_already_taken(cls, schoolyear_id, workshop_id):
        return cls.query.filter(
            cls.schoolyear_id == schoolyear_id,
            cls.workshop_id == workshop_id,
            cls.date == datetime.now().date()
        ).count() != 0

    @classmethod
    def student_assistances(cls, student_id):
        return cls.query.filter(cls.student_id == student_id)
