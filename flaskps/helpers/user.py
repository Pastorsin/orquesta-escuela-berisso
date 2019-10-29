from .validator import Validator, Form
from flaskps.models.user import User

# Validators


class EmailValidator(Validator):

    def __init__(self, field):
        self.email = field

    def validate(self):
        return not User.exist_email(self.email)

    def message(self):
        return 'Error! Ya existe un usuario con ese email.'


class UsernameValidator(Validator):

    def __init__(self, field):
        self.username = field

    def validate(self):
        return not User.exist_username(self.username)

    def message(self):
        return 'Error! Ya existe un usuario con ese nombre de usuario.'


# Form


class UserForm(Form):

    def __init__(self, form):
        super(UserForm, self).__init__(form)

        self.fields['roles'] = form.getlist('roles')

        self.validators.extend([
            EmailValidator(self.fields['email']),
            UsernameValidator(self.fields['username'])
        ])

    def success_message(self):
        return 'Usuario creado con éxito.'
