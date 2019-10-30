# -*- coding: utf-8 -*-
from flask import redirect, request, url_for, flash

from flaskps.extensions.login_manager import login_manager
from flaskps.models.user import User

from flask_login import login_user, logout_user, current_user, login_required

from flaskps.models.role import Role
from flaskps.helpers.user import UserCreateForm, UserEditForm
from flaskps.helpers.constraints import permissions_enabled, permissions_enabled_or_my_profile


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@login_required
@permissions_enabled_or_my_profile('user_index', current_user)
def profile(user_id):
    user = User.query.get(user_id)
    return render_template('user/profile.html', user=user, config=get_web_config(), current_user=current_user)

def login():
    if request.method == 'POST':
        form = request.form
        user = User.query.filter_by(username=form['username']).first()

        message = None

        if user and user.validate_pass(form['password']) and user.is_active:
            if user.is_active:
                login_user(user, remember=True)
                message = 'Se ha iniciado sesión correctamente'
                flash(message, 'info')
                return redirect(url_for('secciones'))
            else:
                message = 'La cuenta se encuentra desactivada, contacte a un administrador'
        else:
            message = 'Nombre de usuario o contraseña invalidos'
        flash(message, 'danger')
        return redirect(url_for('home'))

@login_required
def logout():
    logout_user()
    flash('Se ha cerrado sesión correctamente', 'info')
    return redirect(url_for('home'))
