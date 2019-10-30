from .form import Validator, Form
from flaskps.models.user import User
from flaskps.models.role import Role

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


class CurrentUsernameValidator(UsernameValidator):

    def __init__(self, username, user):
        super(CurrentUsernameValidator, self).__init__(username)
        self.user = user

    def validate(self):
        return super().validate() or self.user.username == self.username


class CurrentEmailValidator(EmailValidator):

    def __init__(self, username, user):
        super(CurrentEmailValidator, self).__init__(username)
        self.user = user

    def validate(self):
        return super().validate() or self.user.email == self.email


# Forms


class UserForm(Form):

    def __init__(self, form):
        super(UserForm, self).__init__(form)
        self.fields['roles'] = form.getlist('roles')

    @property
    def values(self):
        values = self.fields.copy()
        rolenames = self.fields['roles']
        values['roles'] = Role.get_list_by_name(rolenames)
        return values


class UserCreateForm(UserForm):

    def __init__(self, form):
        super(UserCreateForm, self).__init__(form)

        self.validators.extend([
            EmailValidator(self.fields['email']),
            UsernameValidator(self.fields['username'])
        ])

    def success_message(self):
        return 'Usuario creado con éxito.'


class UserEditForm(UserForm):

    def __init__(self, form, user):
        super(UserEditForm, self).__init__(form)

        self.validators.extend([
            CurrentEmailValidator(self.fields['email'], user),
            CurrentUsernameValidator(self.fields['username'], user)
        ])

    def success_message(self):
        return 'Usuario modificado con éxito.'
