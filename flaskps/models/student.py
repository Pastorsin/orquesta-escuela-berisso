from flaskps.extensions.db import db
from .gender import Gender
from .school import School
from .level import Level
from .neighborhood import Neighborhood
from .student_workshop import school_year_workshop_student
from .workshop import Workshop


class Student(db.Model):
    __tablename__ = 'estudiante'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    last_name = db.Column(
        'apellido',
        db.String(30),
        nullable=False
    )

    first_name = db.Column(
        'nombre',
        db.String(20),
        nullable=False
    )

    birth_date = db.Column(
        'fecha_nac',
        db.DateTime,
        nullable=False
    )

    birth_location = db.Column(
        'lugar_nac',
        db.String(255),
        nullable=False
    )

    location_id = db.Column(
        'localidad_id',
        db.Integer,
        nullable=False
    )

    residency = db.Column(
        'domicilio',
        db.String(255),
        nullable=False
    )

    neighborhood_id = db.Column(
        'barrio_id',
        db.Integer,
        db.ForeignKey('barrio.id'),
        nullable=False
    )

    gender_id = db.Column(
        'genero_id',
        db.Integer,
        db.ForeignKey('genero.id'),
        nullable=False
    )

    doc_type_id = db.Column(
        'tipo_doc_id',
        db.Integer,
        nullable=False
    )

    doc_number = db.Column(
        'numero',
        db.Integer,
        nullable=False
    )

    telephone = db.Column(
        'tel',
        db.String(255),
        nullable=False
    )

    school_id = db.Column(
        'escuela_id',
        db.Integer,
        db.ForeignKey('escuela.id'),
        nullable=False
    )

    level_id = db.Column(
        'nivel_id',
        db.Integer,
        db.ForeignKey('nivel.id'),
        nullable=False
    )

    is_active = db.Column(
        'activo',
        db.Boolean,
        nullable=False,
        default=True
    )

    school_years = db.relationship(
        'SchoolYear',
        secondary=school_year_workshop_student,
        lazy='subquery',
        backref=db.backref('students', lazy=True)
    )

    workshops = db.relationship(
        'Workshop',
        secondary=school_year_workshop_student,
        lazy='subquery',
        backref=db.backref('students', lazy=True)
    )

    def __repr__(self):
        return f'<Student {self.first_name}, {self.last_name}>'


    def activate(self):
        self.is_active = True
        db.session.commit()

    def deactivate(self):
        self.is_active = False
        db.session.commit()

    def get_workshops_of_cicle(self, cicle_id):
        return Workshop.query.join(school_year_workshop_student).\
            filter_by(estudiante_id=self.id, ciclo_lectivo_id=cicle_id)
