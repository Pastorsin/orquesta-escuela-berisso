from flask import render_template, flash, redirect, url_for
from flask_login import current_user, login_required
from flaskps.helpers.webconfig import get_web_config
from flaskps.helpers.constraints import permissions_enabled

from flaskps.models.student import Student

SUCCESS_MSG = {
    'deactivate': 'El estudiante {first_name}, {last_name} ha sido desactivado correctamente.',
    'activate': 'El estudiante {first_name}, {last_name} ha sido activado correctamente.'
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
