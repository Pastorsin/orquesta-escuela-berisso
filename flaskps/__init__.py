from flask import Flask, render_template
from flaskps.resources import user
from flaskps.config import Config
from .extensions.db import db
from .extensions.bcrypt import bcrypt

# Configuración inicial de la app
app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
bcrypt.init_app(app)
# Autenticación
#app.add_url_rule("/iniciar_sesion", 'auth_login', auth.login)
#app.add_url_rule("/cerrar_sesion", 'auth_logout', auth.logout)
#app.add_url_rule(
#    "/autenticacion",
#    'auth_authenticate',
#    auth.authenticate,
#    methods=['POST']
#)

# Usuarios
app.add_url_rule("/usuarios", 'user_index', user.index)
app.add_url_rule("/usuarios", 'user_create', user.create, methods=['POST'])
app.add_url_rule("/usuarios/new", 'user_new', user.new)

@app.route("/")
def hello():
    db.create_all()
    return render_template('home/home.html')
