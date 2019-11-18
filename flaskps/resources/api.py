from flaskps.models.school_year import SchoolYear
from flaskps.models.teacher import Teacher
from flaskps.models.student import Student
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


def cicle_workshops_student(estudiante_id, ciclo_id):
    student = Student.query.get(estudiante_id)
    return get_available_workshops(student, ciclo_id)
