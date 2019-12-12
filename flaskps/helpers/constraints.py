from flask import redirect, url_for, flash
from functools import wraps

from flaskps.helpers.assistance import valid_assistance_date


PERMISSION_ERROR = 'No tenés permisos para acceder a esta sección. \
Contacte con un administrador.'

DATE_ERROR = 'La fecha ingresada es inválida'


def permissions_enabled(permisson, user):

    def decorate_view(controller):

        @wraps(controller)
        def wrapper(*args, **kwargs):
            if not user.has_permission(permisson):
                flash(PERMISSION_ERROR, 'danger')
                return redirect(url_for('home'))
            else:
                return controller(*args, **kwargs)
        return wrapper

    return decorate_view


def profile_permissions(permisson, current_user):

    def decorate_view(controller):

        @wraps(permissions_enabled)
        def wrapper(*args, **kwargs):
            user_id = kwargs.get('user_id')
            if user_id == str(current_user.id):
                return controller(*args, **kwargs)
            else:
                permissions = permissions_enabled(permisson, current_user)
                return permissions(controller)(*args, **kwargs)
        return wrapper

    return decorate_view


def date_permissions(permisson, current_user):

    def decorate_view(controller):

        @wraps(permissions_enabled)
        def wrapper(*args, **kwargs):
            if valid_assistance_date(**kwargs):
                permissions = permissions_enabled(permisson, current_user)
                return permissions(controller)(*args, **kwargs)
            else:
                flash(DATE_ERROR, 'danger')
                return redirect(url_for('home'))
        return wrapper

    return decorate_view
