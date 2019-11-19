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

    @classmethod
    def create(cls, data):
        responsable = cls(data)
        db.session.add(responsable)
        db.session.commit()
        return responsable
