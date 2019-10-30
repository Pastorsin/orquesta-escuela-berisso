# -*- coding: utf-8 -*-
from flask import redirect, render_template, request, url_for, abort, flash

from flaskps.extensions.login_manager import login_manager
from flaskps.models.user import User
from flaskps.helpers.webconfig import get_web_config

from flask_login import login_user, logout_user, current_user, login_required

from flaskps.models.role import Role
from flaskps.helpers.user import UserCreateForm, UserEditForm


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@login_required
def index():
    users = User.query.all()
    return render_template('user/index.html', users=users, config=get_web_config(), current_user=current_user)

@login_required
def new(user=None):
    roles = Role.query.all()

    return render_template(
        'user/new.html',
        roles=roles,
        user=user,
        current_user=current_user
    )

@login_required
def create():

    form = UserCreateForm(request.form)

    if form.is_valid():
        User.create(form.values)
        flash(form.success_message(), 'success')
        return redirect(url_for('user_index'))
    else:
        for error in form.error_messages():
            flash(error, 'danger')
        return new(user=form.values)

@login_required
def edit(user_id):
    roles = Role.query.all()
    user = User.query.get(user_id)

    if request.method == 'POST':
        return update(
            form=request.form,
            user=user,
            roles=roles
        )
    else:
        return render_template(
            'user/edit.html',
            roles=roles,
            user=user,
            user_id=user_id,
            current_user=current_user
        )

def update(form, user, roles):
    form = UserEditForm(form, user)

    if form.is_valid():
        user.update(form.values)
        flash(form.success_message(), 'success')
        return redirect(url_for('user_edit', user_id=user.id))
    else:
        for error in form.error_messages():
            flash(error, 'danger')
        return render_template(
            'user/edit.html',
            roles=roles,
            user=form.values,
            user_id=user.id
        )


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
def activateUser(userId):
    user = User.query.get(userId)
    user.activate()
    flash('El usuario %s, %s ha sido activado correctamente.' %
          (user.last_name, user.first_name), 'success')
    return redirect(url_for('user_index'))


@login_required
def deactivateUser(userId):
    if int(userId)!=int(current_user.id):
        user = User.query.get(userId)
        user.deactivate()
        flash('El usuario %s, %s ha sido desactivado correctamente.' %
            (user.last_name, user.first_name), 'success')
    else:
        flash('¡No podes desactivarte a vos mismo!', 'danger')
    return redirect(url_for('user_index'))


@login_required
def logout():
    logout_user()
    flash('Se ha cerrado sesión correctamente', 'info')
    return redirect(url_for('home'))
