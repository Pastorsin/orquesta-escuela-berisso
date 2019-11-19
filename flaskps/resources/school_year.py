from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_required
from flaskps.helpers.webconfig import get_web_config
from flaskps.helpers.constraints import permissions_enabled
from flaskps.helpers.school_year import SchoolYearCreateForm
from flaskps.models.school_year import SchoolYear


SUCCES_MSG = 'Ciclo lectivo generado.'


# @login_required
# @permissions_enabled('teacher_new', current_user)
def new():
    if request.method == 'POST':

        form = SchoolYearCreateForm(request.form)

        if form.is_valid():
            SchoolYear.create(form.values)
            flash(form.success_message(), 'success')
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
