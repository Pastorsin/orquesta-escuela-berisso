# -*- coding: utf-8 -*-
from flask import render_template, flash, redirect, url_for, request
from flaskps.helpers.webconfig import get_web_config
from flask_login import current_user, login_required

from flaskps.models.role import Role
from flaskps.models.user import User
from flaskps.helpers.user import UserCreateForm, UserEditForm
from flaskps.helpers.constraints import permissions_enabled


@login_required
@permissions_enabled('user_activate', current_user)
def activateUser(user_id):
    user = User.query.get(user_id)
    user.activate()
    flash('El usuario %s, %s ha sido activado correctamente.' %
          (user.last_name, user.first_name), 'success')
    return redirect(url_for('user_index'))


@login_required
@permissions_enabled('user_deactivate', current_user)
def deactivateUser(user_id):
    user = User.query.get(user_id)
    user.deactivate()
    flash('El usuario %s, %s ha sido desactivado correctamente.' %
          (user.last_name, user.first_name), 'success')
    return redirect(url_for('user_index'))


@login_required
def index():
    users = User.query.all()
    return render_template('user/index.html', users=users, config=get_web_config(), current_user=current_user)


@login_required
@permissions_enabled('user_new', current_user)
def new(user=None):
    roles = Role.query.all()

    return render_template(
        'user/new.html',
        roles=roles,
        user=user
    )


@login_required
@permissions_enabled('user_create', current_user)
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
@permissions_enabled('user_update', current_user)
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
            config=get_web_config()
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
            user_id=user.id,
            config=get_web_config()
        )
