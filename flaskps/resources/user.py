# -*- coding: utf-8 -*-
from flask import redirect, request, url_for, flash

from flaskps.extensions.login_manager import login_manager
from flaskps.models.user import User

from flask_login import login_user, logout_user, login_required


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


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
