from flaskps.extensions.db import db
from flaskps.models.school_year_workshop import school_year_workshop
from flaskps.models.assistance_student_workshop import AssistanceStudentWorkshop
from datetime import datetime, timedelta


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

    assistances = db.relationship(
        'AssistanceStudentWorkshop',
        backref='schoolyear',
        lazy=True
    )

    courses = db.relationship(
        'TeacherNucleus',
        backref='schoolyear',
        lazy=True
    )

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
        schoolyear = cls.query.filter(
            cls.finish_date >= today, cls.start_date <= today).first()
        return schoolyear

    def get_remaining_workshops(self):
        remaining_workshops = []
        for workshop in self.workshops:
            # Chequeo si no se pasó asistencia todavía el día de hoy y además
            # si corresponde que hoy se pase lista en ese taller (se dan en días particulares)
            if not AssistanceStudentWorkshop.assistance_already_taken(self.id, workshop.id):
                remaining_workshops.append(workshop)
        return remaining_workshops

    def assistance_dates(self, workshop_id, nucleus_id):
        assistance_dates = list(filter(
            lambda date: date.weekday() in self.course_weekdays(workshop_id, nucleus_id),
            self.dates_without_assistance(workshop_id, nucleus_id)
        ))
        return sorted(assistance_dates)

    def course_weekdays(self, workshop_id, nucleus_id):
        return list(map(
            lambda course: course.day.number,
            self.workshop_courses(workshop_id, nucleus_id)
        ))

    def workshop_courses(self, workshop_id, nucleus_id):
        return filter(
            lambda course: course.workshop_id == int(workshop_id),
            self.nucleus_courses(nucleus_id)
        )

    def nucleus_courses(self, nucleus_id):
        return filter(
            lambda course: course.nucleus_id == int(nucleus_id),
            self.courses
        )

    def dates_without_assistance(self, workshop_id, nucleus_id):
        total_dates = set(self.range_dates())
        assistance_dates = set(
            self.dates_workshop_assistances(workshop_id, nucleus_id)
        )
        return total_dates - assistance_dates

    def dates_workshop_assistances(self, workshop_id, nucleus_id):
        return map(
            lambda assistance: assistance.date,
            self.workshop_assistances(workshop_id, nucleus_id)
        )

    def workshop_assistances(self, workshop_id, nucleus_id):
        return filter(
            lambda assistance: assistance.workshop_id == int(workshop_id),
            self.nucleus_assistances(nucleus_id)
        )

    def nucleus_assistances(self, nucleus_id):
        return filter(
            lambda assistance: assistance.nucleus_id == int(nucleus_id),
            self.assistances
        )

    def range_dates(self):
        delta = self.finish_date - self.start_date
        total_days = delta.days + 1
        return [self.start_date + timedelta(days=i) for i in range(total_days)]

    def is_valid_assistance_date(self, a_date, workshop_id, schoolyear_id):
        return a_date in self.assistance_dates(workshop_id, schoolyear_id)
