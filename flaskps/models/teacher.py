from flaskps.extensions.db import db
from .teacher_resp_workshop import school_year_workshop_teacher
from .workshop import Workshop
from .day import Day
from .teacher_nucleus import TeacherNucleus


class Teacher(db.Model):
    __tablename__ = 'docente'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    last_name = db.Column(
        'apellido',
        db.String(255),
        nullable=False
    )

    first_name = db.Column(
        'nombre',
        db.String(255),
        nullable=False
    )

    birth_date = db.Column(
        'fecha_nac',
        db.DateTime,
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

    is_active = db.Column(
        db.Boolean,
        nullable=False,
        default=True
    )

    school_years = db.relationship('SchoolYear', secondary=school_year_workshop_teacher,
                                   lazy='subquery', backref=db.backref('teachers', lazy=True))

    workshops = db.relationship('Workshop', secondary=school_year_workshop_teacher,
                                lazy='subquery', backref=db.backref('teachers', lazy=True))

    def __init__(self, data):
        self.__init_attributes(data)

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
        self.latitude = data['latitude']
        self.longitude = data['longitude']

    def activate(self):
        self.is_active = True
        db.session.commit()
        return self

    def deactivate(self):
        self.is_active = False
        db.session.commit()
        return self

    @classmethod
    def create(cls, data):
        teacher = cls(data)
        db.session.add(teacher)
        db.session.commit()

    def update(self, values):
        self.__init_attributes(values)
        db.session.commit()

    def get_workshops_of_cicle(self, cicle_id):
        return Workshop.query.join(school_year_workshop_teacher).\
            filter_by(docente_id=self.id, ciclo_lectivo_id=cicle_id)

    def get_workshops(self):
        return Workshop.query.join(school_year_workshop_teacher).\
        filter_by(docente_id=self.id)

    def assign_to(self, form_workshops, form_cicle):
        for whp in form_workshops:
            statement = school_year_workshop_teacher.insert().values(
                    docente_id=self.id, ciclo_lectivo_id=form_cicle, taller_id=whp)
            db.session.execute(statement)
        db.session.commit()

    def get_days_of_cicle_whp_nucleus(self, cicle_id, whp_id, nucleus_id):
        return Day.query.join(TeacherNucleus).\
        filter_by(docente_id=self.id, ciclo_lectivo_id=cicle_id, taller_id=whp_id, nucleo_id=nucleus_id)


    # se supone que esto va a asignar los nucleos, algun dia ....
    
    # def assign_to_nucleus(self, form_whp, form_cicle, form_nucleus, week_day):
    #     for whp in form_whp:
    #         statement = TeacherNucleus.insert().values(
    #                 docente_id=self.id, nucleo_id=form_nucleus, ciclo_lectivo_id=form_cicle, dia_semana=week_day)
    #         db.session.execute(statement)
    #     db.session.commit()