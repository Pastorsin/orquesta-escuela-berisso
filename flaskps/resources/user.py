# -*- coding: utf-8 -*-
from flask import redirect, render_template, request, url_for, abort, flash

from flaskps.extensions.login_manager import login_manager
from flaskps.models.user import User
from flaskps.helpers.webconfig import get_web_config

from flask_login import login_user, logout_user, current_user, login_required

from flaskps.models.role import Role
from flaskps.helpers.user import UserForm


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@login_required
def index():
    users = User.query.all()
    return render_template('user/index.html', users=users, config=get_web_config())


def new(user=None):
    if not current_user:
        abort(401)

    roles = Role.query.all()
    return render_template('user/new.html', roles=roles, user=user)


def create():

    form = UserForm(request.form)

    if form.is_valid():
        User.create(form.fields)
        flash(form.success_message(), 'success')
        return redirect(url_for('user_index'))
    else:
        for error in form.error_messages():
            flash(error, 'danger')
        return new(user=form)


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
