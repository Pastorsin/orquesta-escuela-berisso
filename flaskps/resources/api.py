from flaskps.models.school_year import SchoolYear
from flaskps.models.teacher import Teacher
from flaskps.models.student import Student
from flaskps.models.workshop import Workshop
from flaskps.models.nucleus import Nucleus
from flaskps.models.teacher_nucleus import TeacherNucleus
import json


def get_available_workshops(academic, cicle_id):
    occupied_workshops = academic.get_workshops_of_cicle(cicle_id)
    cicle_workshops = SchoolYear.query.get(cicle_id).workshops

    workshops = filter(
        lambda whp: whp not in occupied_workshops, cicle_workshops)
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
    workshops = filter(lambda whp: whp in occupied_workshops, cicle_workshops)
    workshop_dict = {}
    for whp in workshops:
        # Despues tengo q ver como cargar la fecha inicio aca y la de fin tmb
        item = {whp.id: (whp.name, whp.short_name, cicle.semester, whp.id)}
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

    workshops_to_deliver = filter(
        lambda whp: whp not in assigned_workshops, workshops)
    workshop_dict = {}
    for whp in workshops_to_deliver:
        item = {whp.id: (whp.name, whp.short_name)}
        workshop_dict.update(item)
    return json.dumps(workshop_dict)


def get_available_days(academic, cicle_id, taller_id, nucleus_id):
    occupied_days = academic.get_days_of_cicle_whp_nucleus(
        cicle_id, taller_id, nucleus_id)
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


def weekname(a_date):
    weeknames = [
        'Lunes', 'Martes', 'Miercoles', 'Jueves',
        'Viernes', 'Sabado', 'Domingo'
    ]
    return weeknames[a_date.weekday()]


def serialize(assistance_dates):
    dates = []
    for assistance_date in assistance_dates:
        dates.append({
            'dia': weekname(assistance_date),
            'fecha': assistance_date.strftime("%d-%m-%Y")
        })
    return json.dumps(dates)


def get_days_for_workshop_in_schoolyear(ciclo_id, taller_id, nucleo_id):
    current_schoolyear = SchoolYear.query.get(ciclo_id)
    assistance_dates = current_schoolyear.assistance_dates(
        taller_id, nucleo_id)
    return serialize(assistance_dates)


def serialize_nucleus(nucleus):
    data = []
    for nucleu in nucleus:
        data.append({
            'id': nucleu.id,
            'name': nucleu.name
        })
    return json.dumps(data)


def nucleus_of_teacher(workshop_id, schoolyear_id, teacher_id):
    nucleus = TeacherNucleus.nucleus_of(workshop_id, schoolyear_id, teacher_id)
    return serialize_nucleus(nucleus)
