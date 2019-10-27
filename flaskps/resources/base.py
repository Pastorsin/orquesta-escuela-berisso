from flask import render_template
from flaskps.models.webconfig import Webconfig


def index():
    webconfig = Webconfig.query.first()
    return render_template('home/home.html', config=webconfig)


def sections():
    return render_template('home/secciones.html')