from flask import redirect, url_for, flash, request
from functools import wraps

PERMISSION_ERROR = 'No tenés permisos para acceder a esta sección. \
Contacte con un administrador.'


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

def permissions_enabled_or_my_profile(permisson, current_user):

    def decorate_view(controller):

        @wraps(permissions_enabled(permisson,current_user))
        def wrapper(*args, **kwargs):
            if not request.url[-1]==current_user.id:
                flash(PERMISSION_ERROR, 'danger')
                return redirect(url_for('home'))
            else:
                return controller(*args, **kwargs)
        return wrapper

    return decorate_view
