from flaskps.extensions.db import db
from flaskps.models.school_year_workshop import school_year_workshop


class SchoolYear(db.Model):
    __tablename__ = 'ciclo_lectivo'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    start_date = db.Column(
        'fecha_ini',
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

    def __init__(self, data):
        self.__init_attributes(data)

    def __init_attributes(self, data):
        self.start_date = data['starting_date']
        self.finish_date = data['ending_date']
        self.semester = data['semester_id']

    @classmethod
    def create(self, data):
        school_year = self(data)
        db.session.add(school_year)
        db.session.commit()

    def add_workshop(self, workshop):
        self.workshops.append(workshop)
        db.session.commit()

    def has_workshop(self, workshop):
        return workshop in self.workshops    
