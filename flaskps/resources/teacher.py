from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_required
from flaskps.helpers.webconfig import get_web_config
from flaskps.helpers.constraints import permissions_enabled

from flaskps.models.teacher import Teacher
from flaskps.models.gender import Gender

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
@permissions_enabled('teacher_new', current_user)
def new(teacher=None):
    if request.method == 'POST':

        form = TeacherCreateForm(request.form)

        if form.is_valid():
            Teacher.create(form.values)
            flash(form.success_message(), 'success')
            return redirect(url_for('teacher_index'))
        else:
            for error in form.error_messages():
                flash(error, 'danger')
            return new(teacher=form.values)
    
    else:
        generos = Gender.query.all()
        return render_template(
            'teacher/new.html',
            teacher=teacher,
            genders=generos,
        )

@login_required
@permissions_enabled('teacher_update', current_user)
def edit(teacher_id):
    teacher = Teacher.query.get(teacher_id)

    if request.method == 'POST':
        return update(
            form=request.form,
            teacher=teacher,
        )
    else:
        return render_template(
            'teacher/edit.html',
            teacher=teacher,
            teacher_id=teacher_id,
            config=get_web_config()
        )


def update(form, teacher):
    form = TeacherEditForm(form, teacher)

    if form.is_valid():
        teacher.update(form.values)
        flash(form.success_message(), 'success')
        return redirect(url_for('teacher_edit', teacher_id=teacher.id))
    else:
        for error in form.error_messages():
            flash(error, 'danger')
        return render_template(
            'teacher/edit.html',
            teacher=form.values,
            teacher_id=teacher.id,
            config=get_web_config()
        )