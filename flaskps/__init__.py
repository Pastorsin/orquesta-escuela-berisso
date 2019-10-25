from flask import Flask, render_template
from flaskps.config import Config
from .extensions.db import db
from flask_migrate import Migrate
from .extensions.bcrypt import bcrypt

from flaskps.resources import user
from .models.webconfig import Webconfig

# Configuración inicial de la app
app = Flask(__name__)
app.config.from_object(Config)


db.init_app(app)
with app.app_context():
    db.create_all()
migrate = Migrate(app, db)

bcrypt.init_app(app)


# Autenticación
# app.add_url_rule("/iniciar_sesion", 'auth_login', auth.login)
# app.add_url_rule("/cerrar_sesion", 'auth_logout', auth.logout)
app.add_url_rule("/login", 'login', user.login, methods=['POST'])

# Usuarios
app.add_url_rule("/usuarios", 'user_index', user.index)
app.add_url_rule("/usuarios", 'user_create', user.create, methods=['POST'])
app.add_url_rule("/usuarios/new", 'user_new', user.new)


@app.route("/")
def home():
    webconfig = Webconfig.query.first()
    return render_template('home/home.html', config=webconfig)


@app.route("/sections")
def sections():
    return render_template('home/secciones.html')


@app.route("/configuracion")
def webconfig():
    webconfig = Webconfig.query.first()
    return render_template('webconfig/webconfig.html', config=webconfig)
