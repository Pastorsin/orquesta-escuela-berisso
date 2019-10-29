from flask import request, render_template, url_for, redirect, flash
from flaskps.models.webconfig import Webconfig
from flaskps.helpers.webconfig import get_web_config, WebconfigForm


def index():
    return render_template('webconfig/webconfig.html', config=get_web_config())


def edit():
    form = WebconfigForm(request.form)
    if form.is_valid():
        flash(form.success_message(), 'success')
        Webconfig.update(form.values)
    else:
        for error in form.error_messages():
            flash(error, 'danger')
    return redirect(url_for('webconfig'))


def activateSite():
    if(request.method == 'GET'):
        return redirect(url_for('webconfig'))
    else:
        # Habilitar sitio
        return True
