from flask import render_template, flash, redirect, url_for
from flask_login import current_user, login_required
from flaskps.helpers.webconfig import get_web_config

from flaskps.models.student import Student

SUCCESS_MSG = {
    'deactivate': 'El estudiante {first_name}, {last_name} ha sido desactivado correctamente.',
    'activate': 'El estudiante {first_name}, {last_name} ha sido activado correctamente.'
}


@login_required
def index():
    students = Student.query.all()
    return render_template(
        'student/index.html',
        students=students,
        config=get_web_config(),
        current_user=current_user
    )


@login_required
def deactivate(student_id):
    student = Student.query.get(student_id)
    student.deactivate()
    flash(SUCCESS_MSG['deactivate'].format(
        first_name=student.first_name,
        last_name=student.last_name
    ), 'success')
    return redirect(url_for('student_index'))


@login_required
def activate(student_id):
    student = Student.query.get(student_id)
    student.activate()
    flash(SUCCESS_MSG['activate'].format(
        first_name=student.first_name,
        last_name=student.last_name
    ), 'success')
    return redirect(url_for('student_index'))
