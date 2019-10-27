from flask_login import LoginManager

login_manager = LoginManager()
login_manager.login_view = '/'
login_manager.login_message = 'Debe autenticarse para acceder a este contenido'
login_manager.login_message_category = 'danger'
