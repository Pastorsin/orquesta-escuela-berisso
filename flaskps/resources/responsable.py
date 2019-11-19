from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, login_required
from flaskps.helpers.constraints import permissions_enabled
from flaskps.helpers.student import ResponsableEditForm

from flaskps.models.responsable import Responsable
from flaskps.models.gender import Gender

SUCCESS_MSG = {
    'deactivate': 'El responsable {first_name}, {last_name} ha sido desactivado correctamente.',
    'activate': 'El responsable {first_name}, {last_name} ha sido activado correctamente.'
}
ERROR_MSG = {
    'deactivate' : 'Error! Los estudiantes no pueden quedar sin responsables activos'
}


@login_required
@permissions_enabled('student_update', current_user)
def edit(responsable_id):
    responsable = Responsable.query.get(responsable_id)

    if request.method == 'POST':
        return update(
            form=request.form,
            responsable=responsable
        )
    else:
        generos = Gender.query.all()
        return render_template(
            'responsable/edit.html',
            academic=responsable,
            genders=generos,
            academic_id=responsable_id
        )


def update(form, responsable):
    form = ResponsableEditForm(form, responsable)

    if form.is_valid():
        responsable.update(form.values)
        flash(form.success_message(), 'success')
        return redirect(url_for(
            'responsable_profile',
            responsable_id=responsable.id
        ))
    else:
        for error in form.error_messages():
            flash(error, 'danger')
        return render_template(
            'responsable/edit.html',
            academic=form.values,
            genders=Gender.query.all(),
            academic_id=responsable.id
        )


@login_required
@permissions_enabled('student_profile', current_user)
def profile(responsable_id):
    return render_template(
        'academic/profile.html',
        user=Responsable.query.get(responsable_id)
    )


@login_required
@permissions_enabled('student_update', current_user)
def deactivate(responsable_id):
    responsable = Responsable.query.get(responsable_id)
    if responsable.can_deactivated():
        responsable.deactivate()
        flash(SUCCESS_MSG['deactivate'].format(
            first_name=responsable.first_name,
            last_name=responsable.last_name
        ), 'success')
    else:
        flash(ERROR_MSG['deactivate'], 'danger')
    return redirect(url_for(
        'responsable_profile',
        responsable_id=responsable_id
    ))


@login_required
@permissions_enabled('student_update', current_user)
def activate(responsable_id):
    responsable = Responsable.query.get(responsable_id)
    responsable.activate()
    flash(SUCCESS_MSG['activate'].format(
        first_name=responsable.first_name,
        last_name=responsable.last_name
    ), 'success')
    return redirect(url_for(
        'responsable_profile',
        responsable_id=responsable_id
    ))
