from flaskps.models.school_year import SchoolYear
from flaskps.models.teacher import Teacher
from flaskps.models.student import Student
from flaskps.models.workshop import Workshop
from flaskps.models.nucleus import Nucleus
from flaskps.models.day import Day
import json


def get_available_workshops(academic, cicle_id):
    occupied_workshops = academic.get_workshops_of_cicle(cicle_id)
    cicle_workshops = SchoolYear.query.get(cicle_id).workshops

    workshops = filter(lambda whp: whp not in occupied_workshops, cicle_workshops)
    workshop_dict = {}
    for whp in workshops:
        item = {whp.id: (whp.name, whp.short_name)}
        workshop_dict.update(item)
    return json.dumps(workshop_dict)


def cicle_workshops_teacher(docente_id, ciclo_id):
    teacher = Teacher.query.get(docente_id)
    return get_available_workshops(teacher, ciclo_id)

def get_occupied_workshops(academic, ciclo_id):
    occupied_workshops = academic.get_workshops_of_cicle(ciclo_id)
    cicle = SchoolYear.query.get(ciclo_id)
    cicle_workshops = cicle.workshops
    cicle_start_date = cicle.start_date.strftime("%d/%m/%Y")
    cicle_finish_date = cicle.finish_date.strftime("%d/%m/%Y")
    workshops = filter(lambda whp: whp in occupied_workshops, cicle_workshops)
    workshop_dict = {}
    for whp in workshops:
        item = {whp.id: (whp.name, whp.short_name, cicle_start_date, whp.id, cicle_finish_date, ciclo_id)}
        workshop_dict.update(item)
    return json.dumps(workshop_dict)

def cicle_workshops_of_teacher(docente_id, ciclo_id):
    teacher = Teacher.query.get(docente_id)
    return get_occupied_workshops(teacher, ciclo_id)


def cicle_workshops_student(estudiante_id, ciclo_id):
    student = Student.query.get(estudiante_id)
    return get_available_workshops(student, ciclo_id)


def cicle_workshops(ciclo_id):
    workshops = Workshop.query.all()
    assigned_workshops = SchoolYear.query.get(ciclo_id).workshops

    workshops_to_deliver = filter(lambda whp: whp not in assigned_workshops, workshops)
    workshop_dict = {}
    for whp in workshops_to_deliver:
        item = {whp.id: (whp.name, whp.short_name)}
        workshop_dict.update(item)
    return json.dumps(workshop_dict)


def get_available_days(academic, cicle_id, taller_id, nucleus_id):
    occupied_days = academic.get_days_of_cicle_whp_nucleus(cicle_id, taller_id, nucleus_id)
    all_days = Day.query.all()

    days = filter(lambda day: day not in occupied_days, all_days)
    days_dict = {}
    for day in days:
        item = {day.id: (day.name)}
        days_dict.update(item)
    return json.dumps(days_dict)


def cicle_workshops_nucleus_of_teacher(docente_id, ciclo_id, taller_id, nucleo_id):
    teacher = Teacher.query.get(docente_id)
    return get_available_days(teacher, ciclo_id, taller_id, nucleo_id)