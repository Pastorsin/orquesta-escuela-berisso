# -*- coding: utf-8 -*-
from flask import redirect, render_template, request, url_for, abort, flash

from flaskps.extensions.login_manager import login_manager
from flaskps.models.user import User
from flaskps.helpers.webconfig import get_web_config
from flaskps.helpers.forms import not_empty_fields

from flask_login import login_user, logout_user, current_user, login_required

from flaskps.models.role import Role
from flaskps.models.user import User


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@login_required
def index():
    users = User.query.all()
    return render_template('user/index.html', users=users, config=get_web_config())


def new():
    if not current_user:
        abort(401)
    roles = Role.query.all()
    return render_template('user/new.html', roles=roles)


def create():
    ERROR = 'Ha ocurrido un error, verifique los campos ingresados porfavor.'
    SUCCESS = 'Usuario creado con éxito.'
    if not current_user:
        abort(401)

    form = dict(request.form)
    form['roles'] = request.form.getlist('roles')

    if not_empty_fields(form):
        User(form)
        flash(SUCCESS, 'success')
    else:
        flash(ERROR, 'danger')

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
