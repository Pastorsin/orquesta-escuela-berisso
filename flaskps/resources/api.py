from flaskps.models.school_year import SchoolYear
from flaskps.models.teacher import Teacher
import json


def cicle_workshops_docente(docente_id, ciclo_id):
    teacher = Teacher.query.get(docente_id)

    occupied_workshops = teacher.get_workshops_of_cicle(ciclo_id)
    cicle_workshops = SchoolYear.query.get(ciclo_id).workshops

    workshops = filter(lambda whp: whp not in occupied_workshops, cicle_workshops)
    workshop_dict = {}
    for whp in workshops:
        item = {whp.id: (whp.name, whp.short_name)}
        workshop_dict.update(item)
    return json.dumps(workshop_dict)
