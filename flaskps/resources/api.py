from flaskps.models.school_year import SchoolYear
from flaskps.models.teacher import Teacher
from flaskps.models.student import Student
from flaskps.models.workshop import Workshop
from flaskps.models.nucleus import Nucleus
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
    workshops = filter(lambda whp: whp in occupied_workshops, cicle_workshops)
    workshop_dict = {}
    for whp in workshops:
        item = {whp.id: (whp.name, whp.short_name, cicle.semester, whp.id)} #Despues tengo q ver como cargar la fecha inicio aca y la de fin tmb
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

def allsundays(start_date, finish_date, week_day):
    # Las claves deberían estar exactamente igual en la tabla "dia", pero bueno, si no se podría hacer una consulta
    day_values = {
        'Lunes':0,
        'Martes':1,
        'Miercoles':2,
        'Jueves':3,
        'Viernes':4,
        'Sabado':5,
        'Domingo':6,
    }
    d = date(start_date)                    # January 1st
    d += timedelta(days = (day_values[week_day] - d.weekday() + 7) % 7)
    while d<=finish_date:
        yield d
        d += timedelta(days = 7)

def get_days_for_workshop_in_schoolyear(ciclo_id,taller_id):
    # Acá inevitablemente me vas a tener que devolver también el nombre del día para el tema de mostrarlo en la vista, supongo que agregando a la funcion de arriba
    # el parámetro week_day en el yield

    # Fijate de paso de ordenarlo por fecha ;)
    # Acordate también de remover las fechas en las que ya se pasó asistencia, o si no de última mandame otro parámetro como para yo desbloquearlo en el front o ponerlo en rojo
    dates = [
        {
            'dia':'Lunes',
            'fecha':'20-01-2019'
        },
        {
            'dia':'Martes',
            'fecha':'21-01-2019'
        },
        {
            'dia':'Lunes',
            'fecha':'28-01-2019'
        },
        {
            'dia':'Martes',
            'fecha':'29-01-2019'
        },
        {
            'dia':'Miercoles',
            'fecha':'30-01-2019'
        },
    ]
    return json.dumps(dates)