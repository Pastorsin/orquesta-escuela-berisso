from flask import request, render_template, url_for, redirect
from flaskps.models.webconfig import Webconfig


def index():
    webconfig = Webconfig.query.first()
    return render_template('webconfig/webconfig.html', config=webconfig)


def edit():
    config = dict(request.form)
    config['frontend_enabled'] = 'frontend_enabled' in request.form
    Webconfig.update(config)
    return redirect(url_for('webconfig'))
