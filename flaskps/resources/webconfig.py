from flask import request, render_template, url_for, redirect
from flaskps.models.webconfig import Webconfig
from flaskps.helpers.webconfig import get_web_config


def index():
    return render_template('webconfig/webconfig.html', config=get_web_config())


def edit():
    form = dict(request.form)
    if not_empty_fields(form):
        Webconfig.update(form_values(form))
    return redirect(url_for('webconfig'))


def not_empty_fields(form):
    return all(form.values())


def form_values(form):
    form['frontend_enabled'] = 'frontend_enabled' in request.form
    return form
