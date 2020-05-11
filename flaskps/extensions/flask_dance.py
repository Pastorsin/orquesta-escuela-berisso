from flask import flash
from flask_dance.consumer import oauth_authorized, oauth_error
from flask_dance.contrib.google import make_google_blueprint
from flask_login import login_user

from flaskps.models.user import User
from flaskps.config import Config


blueprint = make_google_blueprint(
    client_id=Config.OAUTH_CLIENT_ID,
    client_secret=Config.OAUTH_CLIENT_SECRET,
    scope=["profile", "email"],
)


@oauth_authorized.connect
def google_logged_in(blueprint, token):
    if not token:
        flash("Failed to log in.", category="danger")
        return False

    resp = blueprint.session.get("/oauth2/v1/userinfo")
    if not resp.ok:
        msg = "Failed to fetch user info."
        flash(msg, category="danger")
        return False

    info = resp.json()
    user_email = info["email"]

    # Find this Email in the database
    user = User.query.filter_by(email=user_email).first()
    if user:
        login_user(user)
        flash('Se ha iniciado sesión correctamente', 'info')
    else:
        flash('Lo sentimos, no puede iniciar sesión con esta cuenta de google. Contacte a un administrador', 'danger')

    # Disable Flask-Dance's default behavior for saving the OAuth token
    return False


# notify on OAuth provider danger
@oauth_error.connect
def google_danger(blueprint, message, response):
    msg = ("OAuth error from {name}! " "message={message} response={response}").format(
        name=blueprint.name, message=message, response=response
    )
    flash(msg, category="danger")
