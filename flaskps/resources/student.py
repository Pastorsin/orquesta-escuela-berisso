from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_required

from flaskps.extensions.db import db

from flaskps.helpers.webconfig import get_web_config
from flaskps.helpers.constraints import permissions_enabled

from flaskps.models.student import Student
from flaskps.models.school_year import SchoolYear
from flaskps.models.student_workshop import school_year_workshop_student


SUCCESS_MSG = {
    'deactivate': 'El estudiante {first_name}, {last_name} ha sido desactivado correctamente.',
    'activate': 'El estudiante {first_name}, {last_name} ha sido activado correctamente.',
    'assign': 'El estudiante ha sido asignado a los talleres correctamente.'
}
ERROR_MSG = {
    'assign': 'No se ha enviado el formulario, especifique un ciclo y al menos un taller por favor.',
}


@login_required
@permissions_enabled('student_profile', current_user)
def workshops(student_id):
    student = Student.query.get(student_id)
    return render_template(
        'student/workshops.html',
        academic=student,
        config=get_web_config()
    )


@login_required
@permissions_enabled('student_profile', current_user)
def profile(student_id):
    return 'ndeah'


@login_required
@permissions_enabled('student_index', current_user)
def index():
    students = Student.query.all()
    return render_template(
        'student/index.html',
        students=students,
        config=get_web_config(),
        current_user=current_user
    )


@login_required
@permissions_enabled('student_deactivate', current_user)
def deactivate(student_id):
    student = Student.query.get(student_id)
    student.deactivate()
    flash(SUCCESS_MSG['deactivate'].format(
        first_name=student.first_name,
        last_name=student.last_name
    ), 'success')
    return redirect(url_for('student_index'))


@login_required
@permissions_enabled('student_activate', current_user)
def activate(student_id):
    student = Student.query.get(student_id)
    student.activate()
    flash(SUCCESS_MSG['activate'].format(
        first_name=student.first_name,
        last_name=student.last_name
    ), 'success')
    return redirect(url_for('student_index'))


def add_workshops_to_table(form_workshops, student_id, form_cicle):
    for whp in form_workshops:
        statement = school_year_workshop_student.insert().values(
                estudiante_id=student_id, ciclo_lectivo_id=form_cicle, taller_id=whp)
        db.session.execute(statement)
    db.session.commit()


@login_required
@permissions_enabled('student_update', current_user)
def assign_workshop(student_id):
    if request.method == 'POST':
        form_cicle = request.form.get('cicle')
        form_workshops = request.form.getlist('workshop')
        if form_cicle is not None and form_workshops:
            add_workshops_to_table(form_workshops, student_id, form_cicle)
            flash(SUCCESS_MSG['assign'], 'success')
            return redirect(url_for('student_index'))
        else:
            flash(ERROR_MSG['assign'], 'danger')
            return redirect(url_for('student_assign', student_id=student_id))
    else:
        student = Student.query.get(student_id)
        cicles = SchoolYear.query.all()
        return render_template('student/assign_workshop.html', academic=student, cicles=cicles)
