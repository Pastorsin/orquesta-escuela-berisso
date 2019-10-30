from flask import redirect, url_for, flash
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
