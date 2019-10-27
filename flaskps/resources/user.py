from flask import redirect, render_template, request, url_for, session, abort, flash
from flaskps.models.user import User
from flaskps.helpers.auth import authenticated, validate_pass


def index():
    # if not authenticated(session):
    #    abort(401)

    # User.db = get_db()
    users = User.query.all()
    return render_template('user/index.html', users=users)


def new():
    if not authenticated(session):
        abort(401)

    return render_template('user/new.html')


def create():
    if not authenticated(session):
        abort(401)

    # User.db = get_db()
    # User.create(request.form)
    return redirect(url_for('user_index'))


def login():
    if request.method == 'POST':
        form = request.form
        user = User.query.filter_by(username=form['username']).first()
        if user and validate_pass(user.password, form['password']):
            return user.email
        else:
            flash('Nombre de usuario o contraseña invalidos')
