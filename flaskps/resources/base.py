from flask import render_template


def index():
    return render_template('home/home.html')


def sections():
    return render_template('home/secciones.html')
