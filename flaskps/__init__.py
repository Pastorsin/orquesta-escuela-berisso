from flask import Flask

from flaskps.config import Config
from flaskps.resources import user, base, webconfig, admin, student, teacher

from .extensions.db import db
from .extensions.bcrypt import bcrypt
from .extensions.login_manager import login_manager

from flask_migrate import Migrate

from .models.webconfig import Webconfig


# App initial config
app = Flask(__name__)
app.config.from_object(Config)


db.init_app(app)
with app.app_context():
    db.create_all()

migrate = Migrate(app, db)

login_manager.init_app(app)
bcrypt.init_app(app)


# Jinja2 global context (permanent variables)
@app.context_processor
def global_context():
    config = Webconfig.query.first()
    return dict(config=config)


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
app.add_url_rule("/estudiantes/desactivar/<student_id>", 'deactivate_student', student.deactivate,  methods=['POST'])
app.add_url_rule("/estudiantes/activar/<student_id>", 'activate_student', student.activate,  methods=['POST'])
app.add_url_rule("/estudiantes/<student_id>", 'student_profile', student.profile)
app.add_url_rule("/estudiantes/<student_id>/talleres", 'student_workshops', student.workshops)

# Teachers
app.add_url_rule("/docentes", 'teacher_index', teacher.index)
app.add_url_rule("/docentes/desactivar/<teacher_id>", 'deactivate_teacher', teacher.deactivate,  methods=['POST'])
app.add_url_rule("/docentes/activar/<teacher_id>", 'activate_teacher', teacher.activate,  methods=['POST'])
app.add_url_rule("/docentes/new", 'teacher_new', teacher.new,  methods=['POST', 'GET'])
app.add_url_rule("/docentes/editar/<teacher_id>", 'teacher_edit', teacher.edit,  methods=['POST', 'GET'])
app.add_url_rule("/docentes/<teacher_id>", 'teacher_profile', teacher.profile)
app.add_url_rule("/docentes/<teacher_id>/talleres", 'teacher_workshops', teacher.workshops)
