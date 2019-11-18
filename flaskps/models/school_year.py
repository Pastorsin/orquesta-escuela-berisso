from flaskps.extensions.db import db
from flaskps.models.school_year_workshop import school_year_workshop


class SchoolYear(db.Model):
    __tablename__ = 'ciclo_lectivo'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    start_date = db.Column(
        'fecha_inicio',
        db.Date,
        nullable=False
    )

    finish_date = db.Column(
        'fecha_fin',
        db.Date,
        nullable=False
    )

    semester = db.Column(
        'semestre',
        db.Integer,
        nullable=False
    )

    workshops = db.relationship('Workshop', secondary=school_year_workshop,
                                lazy='subquery', backref=db.backref('school_years', lazy=True))

    @classmethod
    def create(self, data):
        school_year = self(data)
        db.session.add(school_year)
        db.session.commit()
