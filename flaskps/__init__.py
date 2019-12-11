from flask import Flask

from flaskps.config import Config

from flaskps.resources import user, base, webconfig, admin
from flaskps.resources import student, teacher, school_year, responsable
from flaskps.resources import api, instrument, nucleus_map, assistance


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

# Formateador de fechas para Jinja2
def format_datetime(value, format="%d/%m/%Y"):
    """Format a date time to (Default): d Mon YYYY HH:MM P"""
    if value is None:
        return ""
    return value.strftime(format)

app.jinja_env.filters['datetime'] = format_datetime


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
app.add_url_rule("/estudiantes/new", 'student_new', student.new,  methods=['POST', 'GET'])
app.add_url_rule("/estudiantes/editar/<student_id>", 'student_edit', student.edit, methods=['POST', 'GET'])
app.add_url_rule("/estudiantes/<student_id>", 'student_profile', student.profile)
app.add_url_rule("/estudiantes/<student_id>/talleres", 'student_workshops', student.workshops)
app.add_url_rule("/estudiantes/inscribe/<student_id>", 'student_assign', student.assign_workshop, methods=['POST', 'GET'])
app.add_url_rule("/estudiantes/<student_id>/responsables", 'student_responsables', student.responsables)
app.add_url_rule("/estudiantes/<student_id>/responsables/asignar", 'student_assign_responsable', student.assign_responsable, methods=['POST', 'GET'])
app.add_url_rule("/estudiantes/<student_id>/responsables/new", "responsable_new", student.reponsable_new, methods=['POST', 'GET'])
app.add_url_rule("/estudiantes/<student_id>/asistencias", "student_assistances", student.assistances)


# Responsable
app.add_url_rule("/responsable/<responsable_id>", 'responsable_profile', responsable.profile)
app.add_url_rule("/responsable/desactivar/<responsable_id>", 'deactivate_responsable', responsable.deactivate,  methods=['POST'])
app.add_url_rule("/responsable/activar/<responsable_id>", 'activate_responsable', responsable.activate,  methods=['POST'])
app.add_url_rule("/responsable/editar/<responsable_id>", 'responsable_edit', responsable.edit, methods=['POST', 'GET'])


# Teachers
app.add_url_rule("/docentes", 'teacher_index', teacher.index)
app.add_url_rule("/docentes/desactivar/<teacher_id>", 'deactivate_teacher', teacher.deactivate, methods=['POST'])
app.add_url_rule("/docentes/activar/<teacher_id>", 'activate_teacher', teacher.activate, methods=['POST'])
app.add_url_rule("/docentes/new", 'teacher_new', teacher.new, methods=['POST', 'GET'])
app.add_url_rule("/docentes/editar/<teacher_id>", 'teacher_edit', teacher.edit, methods=['POST', 'GET'])
app.add_url_rule("/docentes/<teacher_id>", 'teacher_profile', teacher.profile)
app.add_url_rule("/docentes/<teacher_id>/talleres", 'teacher_workshops', teacher.workshops)
app.add_url_rule("/docentes/inscribe/<teacher_id>", 'teacher_assign', teacher.assign_workshop, methods=['POST', 'GET'])
app.add_url_rule("/docentes/asignar_nucleo/<teacher_id>", 'teacher_assign_nucleus', teacher.assign_nucleus, methods=['POST', 'GET'])


# API
app.add_url_rule('/api/docente/<docente_id>/ciclo/<ciclo_id>', 'cicle_workshops_teacher', api.cicle_workshops_teacher)
app.add_url_rule('/api/docente/<docente_id>/ciclo_taller/<ciclo_id>', 'cicle_workshops_of_teacher', api.cicle_workshops_of_teacher)
app.add_url_rule('/api/docente/<docente_id>/ciclo/<ciclo_id>/taller/<taller_id>/nucleo/<nucleo_id>', 'cicle_workshops_nucleus_of_teacher', api.cicle_workshops_nucleus_of_teacher)
app.add_url_rule('/api/estudiante/<estudiante_id>/ciclo/<ciclo_id>', 'cicle_workshops_student', api.cicle_workshops_student)
app.add_url_rule('/api/ciclo_lectivo/<ciclo_id>', 'cicle_workshops', api.cicle_workshops)
app.add_url_rule('/api/fechas/<ciclo_id>/<taller_id>/<nucleo_id>','workshop_dates',api.get_days_for_workshop_in_schoolyear)
app.add_url_rule('/api/nucleos/<workshop_id>/<schoolyear_id>/<teacher_id>', 'nucleus_courses', api.nucleus_of_teacher)


# SchoolYear
app.add_url_rule("/ciclo_lectivo/new", 'schoolyear_new', school_year.new, methods=['POST', 'GET'])
app.add_url_rule("/ciclo_lectivo/assign_workshop", 'schoolyear_assign_workshop', school_year.assign_workshop, methods=['POST', 'GET'])


# Instruments
app.add_url_rule("/instrumentos", 'instrument_index', instrument.index)
app.add_url_rule("/instrumentos/new", 'instrument_new', instrument.new, methods=['POST', 'GET'])
app.add_url_rule("/instrumentos/desactivar/<instrument_id>", 'deactivate_instrument', instrument.deactivate,  methods=['POST'])
app.add_url_rule("/instrumentos/activar/<instrument_id>", 'activate_instrument', instrument.activate,  methods=['POST'])
app.add_url_rule("/instrumentos/<instrument_id>", 'instrument_profile', instrument.profile)
app.add_url_rule("/instrumentos/editar/<instrument_id>", 'instrument_edit', instrument.edit, methods=['POST', 'GET'])
app.add_url_rule("/instrumentos/editar/<instrument_id>/imagen", 'instrument_image_edit', instrument.edit_image, methods=['POST', 'GET'])


# Map
app.add_url_rule("/mapa", 'nucleus_map', nucleus_map.index)

# Assistance
app.add_url_rule("/asistencia", 'assistance_list', assistance.index)
app.add_url_rule("/asistencia/<schoolyear_id>/<workshop_id>/<nucleus_id>/<assistance_date>", 'assistance_register', assistance.register_assistance, methods=['POST', 'GET'])
