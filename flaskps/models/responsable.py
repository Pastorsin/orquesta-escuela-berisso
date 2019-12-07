from flaskps.extensions.db import db


class Responsable(db.Model):
    __tablename__ = 'responsable'

    id = db.Column(
        db.Integer,
        autoincrement=True,
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

    location_id = db.Column(
        'localidad_id',
        db.Integer
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
        'activo',
        db.Boolean,
        nullable=False,
        default=True
    )

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

    @classmethod
    def create(cls, data):
        responsable = cls(data)
        db.session.add(responsable)
        db.session.commit()
        return responsable

    def activate(self):
        self.is_active = True
        db.session.commit()

    def deactivate(self):
        self.is_active = False
        db.session.commit()

    def update(self, values):
        self.__init_attributes(values)
        db.session.commit()

    def can_deactivated(self):
        return all(map(
            lambda student: student.more_responsables_active_that(self),
            self.students
        ))

    @classmethod
    def all_except(cls, responsables):
        return Responsable.query.filter(
            ~Responsable.id.in_(cls.responsables_id(responsables))
        )

    @classmethod
    def responsables_id(cls, responsables):
        return list(map(lambda responsable: int(responsable.id), responsables))

    @property
    def full_name(self):
        return f"{self.last_name}, {self.first_name}"
