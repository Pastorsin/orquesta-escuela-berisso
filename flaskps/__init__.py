from flask import Flask

from flaskps.config import Config
from flaskps.resources import user, base, webconfig, admin

from .extensions.db import db
from .extensions.bcrypt import bcrypt
from .extensions.login_manager import login_manager

from flask_migrate import Migrate


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
app.add_url_rule('/cerrar_sesion', 'logout', user.logout)
app.add_url_rule('/iniciar_sesion', 'login', user.login, methods=['POST'])

# Usuarios
app.add_url_rule("/usuarios", 'user_index', admin.index)
app.add_url_rule("/usuarios/new", 'user_create', admin.create, methods=['POST'])
app.add_url_rule("/usuarios/new", 'user_new', admin.new)
app.add_url_rule("/usuarios/editar/<user_id>", 'user_edit', admin.edit,  methods=['GET', 'POST'])
app.add_url_rule("/desactivar_usuario/<userId>", 'deactivate_user', admin.deactivateUser)
app.add_url_rule("/activar_usuario/<userId>", 'activate_user', admin.activateUser)

# Base
app.add_url_rule('/', 'home', base.index)
app.add_url_rule('/secciones', 'secciones', base.sections)

# Configuracion
app.add_url_rule("/configuracion", 'webconfig', webconfig.index)
app.add_url_rule("/configuracion/editar", 'webconfig_edit', webconfig.edit, methods=['POST'])
