from functools import wraps

from flask_login import current_user

from flask import abort


def auth_required(controller):

    @wraps(controller)
    def decorate(*args, **kwargs):
        if current_user.is_authenticated:
            return controller(*args, **kwargs)
        else:
            abort(401)
    return decorate

def permissions_enabled(permisson):

    def decorate_view(controller):

        @wraps(controller)
        def wrapper(*args, **kwargs):
            if not current_user.has_permission(permisson):
                abort(403)
            else:
                return controller(*args, **kwargs)
        return wrapper

    return decorate_view
