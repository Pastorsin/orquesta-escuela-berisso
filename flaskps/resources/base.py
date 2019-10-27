from flask import render_template
from flaskps.models.webconfig import Webconfig
from flask_login import current_user


def index():
    if current_user.is_authenticated:
        return render_template('home/secciones.html')

    webconfig = Webconfig.query.first()
    return render_template('home/home.html', config=webconfig)


def sections():
    return render_template('home/secciones.html')
