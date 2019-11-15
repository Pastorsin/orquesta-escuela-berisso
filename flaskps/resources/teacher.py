from flask import render_template, flash, redirect, url_for
from flask_login import current_user, login_required
from flaskps.helpers.webconfig import get_web_config
from flaskps.helpers.constraints import permissions_enabled

from flaskps.models.teacher import Teacher

SUCCESS_MSG = {
    'deactivate': 'El docente {first_name}, {last_name} ha sido desactivado correctamente.',
    'activate': 'El docente {first_name}, {last_name} ha sido activado correctamente.'
}


@login_required
@permissions_enabled('teacher_index', current_user)
def index():
    teachers = Teacher.query.all()
    return render_template(
        'teacher/index.html',
        teachers=teachers,
        config=get_web_config(),
        current_user=current_user
    )


@login_required
@permissions_enabled('teacher_deactivate', current_user)
def deactivate(teacher_id):
    teacher = Teacher.query.get(teacher_id)
    teacher.deactivate()
    flash(SUCCESS_MSG['deactivate'].format(
        first_name=teacher.first_name,
        last_name=teacher.last_name
    ), 'success')
    return redirect(url_for('teacher_index'))


@login_required
@permissions_enabled('teacher_activate', current_user)
def activate(teacher_id):
    teacher = Teacher.query.get(teacher_id)
    teacher.activate()
    flash(SUCCESS_MSG['activate'].format(
        first_name=teacher.first_name,
        last_name=teacher.last_name
    ), 'success')
    return redirect(url_for('teacher_index'))

@login_required
@permissions_enabled('teacher_create', current_user)
def create():

    form = TeacherCreateForm(request.form)

    if form.is_valid():
        Teacher.create(form.values)
        flash(form.success_message(), 'success')
        return redirect(url_for('teacher_index'))
    else:
        for error in form.error_messages():
            flash(error, 'danger')
        return new(teacher=form.values)
