from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_required

from flaskps.helpers.webconfig import get_web_config
from flaskps.helpers.constraints import permissions_enabled
from flaskps.helpers.student import StudentCreateForm, ResponsableCreateForm
from flaskps.helpers.student import StudentEditForm

from flaskps.models.student import Student
from flaskps.models.school_year import SchoolYear
from flaskps.models.gender import Gender
from flaskps.models.neighborhood import Neighborhood
from flaskps.models.school import School
from flaskps.models.level import Level
from flaskps.models.responsable import Responsable

import json


SUCCESS_MSG = {
    'deactivate': 'El estudiante {first_name}, {last_name} ha sido desactivado correctamente.',
    'activate': 'El estudiante {first_name}, {last_name} ha sido activado correctamente.',
    'assign': 'El estudiante ha sido asignado a los talleres correctamente.',
    'assign_responsable': 'El responsable ha sido asignado correctamente.'
}
ERROR_MSG = {
    'assign': 'No se ha enviado el formulario, especifique un ciclo y al menos un taller por favor.',
    'assign_responsable': 'Error! Ya existe ese responsable asignado para el alumno'
}


@login_required
@permissions_enabled('student_update', current_user)
def assign_responsable(student_id):
    student = Student.query.get(student_id)
    if request.method == 'POST':
        responsable_id = request.form['responsable_id']
        responsable = Responsable.query.get(responsable_id)
        if student.has_responsable(responsable):
            flash(ERROR_MSG['assign_responsable'], 'danger')
        else:
            student.add_responsable(responsable)
            flash(SUCCESS_MSG['assign_responsable'], 'success')
    return render_template(
        'student/assign_responsable.html',
        student=student,
        responsables=Responsable.all_except(student.responsables)
    )


@login_required
@permissions_enabled('student_update', current_user)
def reponsable_new(student_id):
    student = Student.query.get(student_id)
    if request.method == 'POST':
        form = ResponsableCreateForm(request.form)

        if form.is_valid():
            responsable = form.save()
            student.add_responsable(responsable)
            flash(form.success_message(), 'success')
            return redirect(url_for(
                'student_responsables',
                student_id=student.id
            ))
        else:
            for error in form.error_messages():
                flash(error, 'danger')
            return render_template(
                'responsable/new.html',
                academic=form.values,
                student=student,
                genders=Gender.query.all()
            )
    else:
        return render_template(
            'responsable/new.html',
            academic=None,
            student=student,
            genders=Gender.query.all(),
        )


@login_required
@permissions_enabled('student_update', current_user)
def edit(student_id):
    student = Student.query.get(student_id)

    if request.method == 'POST':
        return update(
            form=request.form,
            student=student
        )
    else:
        return render_template(
            'student/edit.html',
            academic=student,
            genders=Gender.query.all(),
            schools=School.query.all(),
            levels=Level.query.all(),
            neighborhoods=Neighborhood.query.all()
        )


def update(form, student):
    form = StudentEditForm(form, student)

    if form.is_valid():
        student.update(form.values)
        flash(form.success_message(), 'success')
        return redirect(url_for(
            'student_edit',
            student_id=student.id
        ))
    else:
        for error in form.error_messages():
            flash(error, 'danger')
        return render_template(
            'responsable/edit.html',
            academic=form.values,
            genders=Gender.query.all(),
            schools=School.query.all(),
            levels=Level.query.all(),
            neighborhoods=Neighborhood.query.all()
        )


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
def responsables(student_id):
    return render_template(
        'responsable/index.html',
        student=Student.query.get(student_id)
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


@login_required
@permissions_enabled('student_update', current_user)
def assign_workshop(student_id):
    student = Student.query.get(student_id)
    if request.method == 'POST':
        form_cicle = request.form.get('cicle')
        form_workshops = request.form.getlist('workshop')
        if form_cicle is not None and form_workshops:
            student.assign_to(form_workshops, form_cicle)
            flash(SUCCESS_MSG['assign'], 'success')
            return redirect(url_for('student_index'))
        else:
            flash(ERROR_MSG['assign'], 'danger')
            return redirect(url_for('student_assign', student_id=student_id))
    else:
        cicles = SchoolYear.query.all()
        return render_template('student/assign_workshop.html', academic=student, cicles=cicles)


@login_required
@permissions_enabled('student_new', current_user)
def new():
    if request.method == 'POST':
        print(json.dumps(request.get_json(), indent=4))
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
            responsables=Responsable.query.all(),
            genders=Gender.query.all(),
            schools=School.query.all(),
            levels=Level.query.all(),
            neighborhoods=Neighborhood.query.all()
        )
