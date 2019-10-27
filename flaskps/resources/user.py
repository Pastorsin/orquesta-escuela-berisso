# -*- coding: utf-8 -*-
from flask import redirect, render_template, request, url_for, abort, flash

from flaskps.extensions.login_manager import login_manager
from flaskps.models.user import User

from flask_login import login_user, logout_user, current_user, login_required


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


def index():
    # if not authenticated(session):
    #    abort(401)

    # User.db = get_db()
    users = User.query.all()
    return render_template('user/index.html', users=users)


def new():
    if current_user:
        abort(401)

    return render_template('user/new.html')


def create():
    if current_user:
        abort(401)

    # User.db = get_db()
    # User.create(request.form)
    return redirect(url_for('user_index'))


def login():
    if request.method == 'POST':
        form = request.form
        user = User.query.filter_by(username=form['username']).first()

        if user and user.validate_pass(form['password']):
            login_user(user, remember=True)
            flash('Se ha iniciado sesión correctamente', 'info')
            return redirect(url_for('secciones'))
        flash('Nombre de usuario o contraseña invalidos', 'danger')
        return redirect(url_for('home'))


@login_required
def logout():
    logout_user()
    flash('Se ha cerrado sesión correctamente', 'info')
    return redirect(url_for('home'))
