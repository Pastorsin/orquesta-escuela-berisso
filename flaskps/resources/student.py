from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_required
from flaskps.helpers.webconfig import get_web_config
from flaskps.helpers.constraints import permissions_enabled
from flaskps.helpers.student import ResponsableCreateForm, StudentCreateForm
from flaskps.helpers.form import Form

from flaskps.models.student import Student
from flaskps.models.gender import Gender
from flaskps.models.neighborhood import Neighborhood
from flaskps.models.school import School
from flaskps.models.level import Level

import json


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


def new():
    neighborhoods = Neighborhood.query.all()
    schools = School.query.all()
    genders = Gender.query.all()
    levels = Level.query.all()

    if request.method == 'POST':
        student_form = StudentCreateForm(request.get_json())

        if student_form.is_valid():
            student_form.save()
            flash(student_form.success_message(), 'success')
        else:
            for error in student_form.invalid_messages():
                flash(error, 'danger')

        return json.dumps([
            {'success': student_form.is_valid()},
            {'messages': render_template('forms/messages.html')},
            200,
            {'ContentType': 'application/json'}
        ])
    else:
        return render_template(
            'student/new.html',
            academic=None,
            genders=genders,
            schools=schools,
            levels=levels,
            neighborhoods=neighborhoods
        )
