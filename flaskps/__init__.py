from flask import Flask

from flaskps.config import Config
from flaskps.resources import user, base, webconfig

from .extensions.db import db
from .extensions.bcrypt import bcrypt
from .extensions.login_manager import login_manager

from flask_migrate import Migrate

<<<<<<< HEAD
from flaskps.resources import user, webconfig
from .helpers.webconfig import web_config
=======
>>>>>>> develop

# Configuración inicial de la app
app = Flask(__name__)
app.config.from_object(Config)


db.init_app(app)
with app.app_context():
    db.create_all()

migrate = Migrate(app, db)

login_manager.init_app(app)
bcrypt.init_app(app)


# Autenticación
# app.add_url_rule('/cerrar_sesion', 'auth_logout', auth.logout)
app.add_url_rule('/iniciar_sesion', 'login', user.login, methods=['POST'])

# Usuarios
app.add_url_rule("/usuarios", 'user_index', user.index)
app.add_url_rule("/usuarios", 'user_create', user.create, methods=['POST'])
app.add_url_rule("/usuarios/new", 'user_new', user.new)


@app.route("/")
def home():
    webconfig = web_config()
    return render_template('home/home.html', config=webconfig)


@app.route("/sections")
def sections():
    webconfig = web_config()
    return render_template('home/secciones.html', config=webconfig)


# Base
app.add_url_rule('/', 'home', base.index)
app.add_url_rule('/secciones', 'secciones', base.sections)

# Configuracion
app.add_url_rule("/configuracion", 'webconfig', webconfig.index)
app.add_url_rule("/configuracion/editar", 'webconfig_edit', webconfig.edit, methods=['POST'])
