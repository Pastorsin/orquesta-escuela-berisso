from flask import Flask

from flaskps.config import Config
from flaskps.resources import user, base, webconfig, admin, student

from .extensions.db import db
from .extensions.bcrypt import bcrypt
from .extensions.login_manager import login_manager

from flask_migrate import Migrate


# App initial config
app = Flask(__name__)
app.config.from_object(Config)


db.init_app(app)
with app.app_context():
    db.create_all()

migrate = Migrate(app, db)

login_manager.init_app(app)
bcrypt.init_app(app)


# Auth
app.add_url_rule('/cerrar_sesion', 'logout', user.logout)
app.add_url_rule('/iniciar_sesion', 'login', user.login, methods=['POST'])

# Users
app.add_url_rule("/usuarios", 'user_index', admin.index)
app.add_url_rule("/usuarios/new", 'user_create', admin.create, methods=['POST'])
app.add_url_rule("/usuarios/new", 'user_new', admin.new)
app.add_url_rule("/usuarios/editar/<user_id>", 'user_edit', admin.edit,  methods=['GET', 'POST'])
app.add_url_rule("/desactivar_usuario/<user_id>", 'deactivate_user', admin.deactivateUser)
app.add_url_rule("/activar_usuario/<user_id>", 'activate_user', admin.activateUser)
app.add_url_rule("/usuario/<user_id>", 'user_profile', user.profile)


# Sections
app.add_url_rule('/', 'home', base.index)
app.add_url_rule('/secciones', 'secciones', base.sections)

# Webconfig
app.add_url_rule("/configuracion", 'webconfig', webconfig.index)
app.add_url_rule("/configuracion/editar", 'webconfig_edit', webconfig.edit, methods=['POST'])

# Students
app.add_url_rule("/estudiantes", 'student_index', student.index)