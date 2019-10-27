from flask import render_template, url_for, redirect
from flaskps.helpers.webconfig import get_web_config
from flask_login import current_user, login_required


def index():
    if current_user.is_authenticated:
        return redirect(url_for('secciones'))
    return render_template('home/home.html', config=get_web_config())


@login_required
def sections():
    return render_template('home/secciones.html', config=get_web_config())
