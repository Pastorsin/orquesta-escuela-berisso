from flaskps.extensions.login_manager import login_manager
from flask_login import current_user
from flaskps.models.user import User


def authenticated(session):
    return current_user


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
