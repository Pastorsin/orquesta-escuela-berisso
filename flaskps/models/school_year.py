from flaskps.extensions.db import db
from flaskps.models.school_year_workshop import school_year_workshop
from flaskps.models.assistance_student_workshop import AssistanceStudentWorkshop
from datetime import datetime


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

    def assign_workshops(self, form_workshops):
        for whp in form_workshops:
            statement = school_year_workshop.insert().values(
                ciclo_lectivo_id=self.id, taller_id=whp)
            db.session.execute(statement)
        db.session.commit()
    
    @classmethod
    def get_current_schoolyear(cls):
        today = datetime.now()
        schoolyear = cls.query.filter(cls.finish_date>=today,cls.start_date<=today).first()
        return schoolyear

    def get_remaining_workshops(self):
        remaining_workshops = []
        for workshop in self.workshops:
            # Chequeo si no se pasó asistencia todavía el día de hoy y además
            # si corresponde que hoy se pase lista en ese taller (se dan en días particulares)
            if not AssistanceStudentWorkshop.assistance_already_taken(self.id,workshop.id):
                remaining_workshops.append(workshop)
        return remaining_workshops