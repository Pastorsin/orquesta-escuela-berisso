from flaskps.extensions.db import db
from .gender import Gender
from .school import School
from .level import Level
from .neighborhood import Neighborhood
from .responsable import Responsable
from .student_workshop import school_year_workshop_student
from .workshop import Workshop
from .responsable_student import responsable_student


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

    latitude = db.Column(
        'latitud',
        db.String(255),
        nullable=False
    )

    longitude = db.Column(
        'longitud',
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

    responsables = db.relationship(
        'Responsable',
        secondary=responsable_student,
        lazy='subquery',
        backref=db.backref('students', lazy=True)
    )

    def __init__(self, data):
        self.__init_attributes(data)
        self.__init_relationships(data)

    def __init_attributes(self, data):
        self.last_name = data['last_name']
        self.first_name = data['first_name']
        self.birth_date = data['birth_date']
        self.location_id = data['location_id']
        self.residency = data['residency']
        self.gender_id = data['gender_id']
        self.doc_type_id = data['doc_type_id']
        self.doc_number = data['doc_number']
        self.telephone = data['telephone']
        self.gender_id = data['gender_id']
        self.school_id = data['school_id']
        self.neighborhood_id = data['neighborhood_id']
        self.birth_location = data['birth_location']
        self.level_id = data['level_id']
        self.latitude = data['latitude']
        self.longitude = data['longitude']

    def __init_relationships(self, data):
        self.responsables = self.__responsables_by_id(data['responsables_id'])

    def __responsables_by_id(self, responsables_id):
        return [Responsable.query.get(r_id) for r_id in responsables_id]

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

    @classmethod
    def create(cls, data):
        student = cls(data)
        db.session.add(student)
        db.session.commit()

    def update(self, values):
        self.__init_attributes(values)
        db.session.commit()

    def more_responsables_active_that(self, responsable):
        return any(map(
            lambda r: r.is_active, self.other_responsables(responsable)
        ))

    def other_responsables(self, responsable):
        return filter(
            lambda r: r.id != responsable.id, self.responsables
        )

    def add_responsable(self, responsable):
        self.responsables.append(responsable)
        db.session.commit()

    def assign_to(self, form_workshops, form_cicle):
        for whp in form_workshops:
            statement = school_year_workshop_student.insert().values(
                    estudiante_id=self.id, ciclo_lectivo_id=form_cicle, taller_id=whp)
            db.session.execute(statement)
        db.session.commit()

    def has_responsable(self, responsable):
        return responsable in self.responsables
