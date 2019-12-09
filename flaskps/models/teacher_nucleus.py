from flaskps.extensions.db import db


class TeacherNucleus(db.Model):
    __tablename__ = 'docente_nucleo_taller_ciclo'

    teacher_id = db.Column(
        'docente_id',
        db.Integer,
        db.ForeignKey('docente.id'),
        primary_key=True
    )

    nucleus_id = db.Column(
        'nucleo_id',
        db.Integer,
        db.ForeignKey('nucleo.id'),
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

    day_id = db.Column(
        'dia_id',
        db.Integer,
        db.ForeignKey('dia.id'),
        primary_key=True
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

    def __init_attributes(self, teacher_id, nucleus_id, schoolyear_id, workshop_id, day_id):
        self.teacher_id = teacher_id
        self.nucleus_id = nucleus_id
        self.schoolyear_id = schoolyear_id
        self.workshop_id = workshop_id
        self.day_id = day_id

    @classmethod
    def create(cls, teacher_id, nucleus_id, schoolyear_id, workshop_id, day_id):
        teacherNucleus = cls(data)
        db.session.add(teacherNucleus)
        db.session.commit()
