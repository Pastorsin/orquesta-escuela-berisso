# -*- coding: utf-8 -*-
from flask import redirect, render_template, request, url_for, session, abort, flash
from flaskps.models.user import User
from flaskps.helpers.auth import authenticated
from flask_login import login_user


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

        if user and user.validate_pass(form['password']):
            login_user(user, remember=True)
            flash('Se ha iniciado sesión correctamente')
            return redirect(url_for('secciones'))
        flash('Nombre de usuario o contraseña invalidos')
        return redirect(url_for('home'))
