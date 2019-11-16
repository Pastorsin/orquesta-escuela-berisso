from flaskps.extensions.db import db
from .teacher_resp_workshop import school_year_workshop


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

    school_years = db.relationship('SchoolYear', secondary=school_year_workshop,
                                   lazy='subquery', backref=db.backref('teachers', lazy=True))

    workshops = db.relationship('Workshop', secondary=school_year_workshop,
                                lazy='subquery', backref=db.backref('teachers', lazy=True))

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
