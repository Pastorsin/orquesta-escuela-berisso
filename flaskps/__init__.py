from flask import Flask, render_template
from flaskps.config import Config
from .extensions.db import db
from flask_migrate import Migrate
from .extensions.bcrypt import bcrypt

from flaskps.resources import user

# Configuración inicial de la app
app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)

bcrypt.init_app(app)


# Autenticación
# app.add_url_rule("/iniciar_sesion", 'auth_login', auth.login)
# app.add_url_rule("/cerrar_sesion", 'auth_logout', auth.logout)

# Usuarios
app.add_url_rule("/usuarios", 'user_index', user.index)
app.add_url_rule("/usuarios", 'user_create', user.create, methods=['POST'])
app.add_url_rule("/usuarios/new", 'user_new', user.new)


@app.route("/")
def hello():
    db.create_all()
    return render_template('home/home.html')


@app.route("/sections")
def sections():
    return render_template('home/secciones.html')
