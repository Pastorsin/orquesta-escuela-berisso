from .form import Validator, Form
from datetime import date, datetime


# Validators

class BirthdateValidator(Validator):

    def __init__(self, field):
        self.birthdate = field

    def validate(self):
        return self.birthdate and datetime.strptime(self.birthdate,'%Y-%m-%d').date() < date.today()

    def message(self):
        return 'Error! La fecha de nacimiento no puede ser posterior a la fecha actual.'


class DocNumberValidator(Validator):

    def __init__(self, field):
        self.docnumber = field

    def validate(self):
        return self.docnumber.isdigit()

    def message(self):
        return 'Error! El tipo de documento debe ser numérico.'


# Forms

class TeacherForm(Form):

    def __init__(self, form):
        super(TeacherForm, self).__init__(form)

    @property
    def values(self):
        values = self.fields.copy()
        return values


class TeacherCreateForm(TeacherForm):

    def __init__(self, form):
        super(TeacherCreateForm, self).__init__(form)

        self.validators.extend([
            BirthdateValidator(self.fields['birth_date']),
            DocNumberValidator(self.fields['doc_number'])
        ])

    def success_message(self):
        return 'Docente creado con éxito.'


class TeacherEditForm(TeacherForm):

    def __init__(self, form, user):
        super(TeacherEditForm, self).__init__(form)

        self.validators.extend([
            BirthdateValidator(self.fields['birth_date']),
            DocNumberValidator(self.fields['doc_number'])
        ])

    def success_message(self):
        return 'Docente modificado con éxito.'
