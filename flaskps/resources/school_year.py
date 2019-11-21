from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_required

from flaskps.extensions.db import db

from flaskps.helpers.webconfig import get_web_config
from flaskps.helpers.constraints import permissions_enabled
from flaskps.helpers.school_year import SchoolYearCreateForm
from flaskps.models.school_year import SchoolYear
from flaskps.models.workshop import Workshop
from flaskps.models.school_year_workshop import school_year_workshop


SUCCESS_MSG = {
    'new_cicle':'Ciclo lectivo generado',
    'assign':'Taller asignado correctamente'
}
ERROR_MSG = {
    'assign': 'No se ha enviado el formulario, especifique un ciclo y al menos un taller por favor.',
}

@login_required
@permissions_enabled('schoolyear_new', current_user)
def new():
    if request.method == 'POST':

        form = SchoolYearCreateForm(request.form)

        if form.is_valid():
            SchoolYear.create(form.values)
            flash(SUCCESS_MSG['new_cicle'], 'success')
            return redirect(url_for('schoolyear_new'))
        else:
            for error in form.error_messages():
                flash(error, 'danger')
            return render_template(
                'schoolyear/new.html',
                academic=form.values,
            )

    else:
        return render_template(
            'schoolyear/new.html',
            academic=None,
        )

def add_workshops_to_table(form_workshops, form_cicle):
    for whp in form_workshops:
        statement = school_year_workshop.insert().values(
            ciclo_lectivo_id=form_cicle, taller_id=whp)
        db.session.execute(statement)
    db.session.commit()

@login_required
@permissions_enabled('schoolyear_update', current_user)
def assign_workshop():
    if request.method == 'POST':
        form_cicle = request.form.get('cicle')
        form_workshops = request.form.get('workshop')
        if form_cicle is not None and form_workshops is not None:
            add_workshops_to_table(form_workshops, form_cicle)
            flash(SUCCESS_MSG['assign'], 'success')
            return redirect(url_for('secciones'))
        else:
            flash(ERROR_MSG['assign'], 'danger')
            return redirect(url_for('secciones', 1))
    else:
        cicles = SchoolYear.query.all()
        workshop = Workshop.query.all()
        return render_template('schoolyear/assign_workshop.html', cicles=cicles, workshop= workshop)
