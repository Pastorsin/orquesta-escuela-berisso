from .teacher import TeacherCreateForm, TeacherEditForm
from .form import Form, Validator
from flaskps.models.student import Student
from flaskps.models.responsable import Responsable


class ResponsableCreateForm(TeacherCreateForm):

    @classmethod
    def forms(cls, responsables_data):
        forms = [cls(data) for data in responsables_data]
        return forms

    def save(self):
        responsable = Responsable.create(self.values)
        return responsable

    def success_message(self):
        return 'Responsable creado con éxito'


class ResponsableEditForm(TeacherEditForm):

    def success_message(self):
        return 'Responsable modificado con éxito'


class StudentEditForm(TeacherEditForm):

    def success_message(self):
        return 'Estudiante modificado con éxito'


class ResponsablesFieldsValidator(Validator):

    def __init__(self, responsables):
        self.responsables = responsables

    def validate(self):
        return bool(self.responsables)

    def message(self):
        return 'Error! Se debe seleccionar o crear algún responsable.'


class StudentCreateForm(TeacherCreateForm):

    def __init__(self, form):
        super(StudentCreateForm, self).__init__(form['student'])
        self.responsables_id = form['responsable']['checked']
        self.responsables_forms = ResponsableCreateForm.forms(
            form['responsable']['created']
        )
        self.validators.extend([
            ResponsablesFieldsValidator(
                self.responsables_id + self.responsables_forms
            )
        ])

    def success_message(self):
        return 'Estudiante creado con éxito'

    def save(self):
        self.responsables_saved = Form.save(self.responsables_forms)
        student = Student.create(self.values)
        return student

    def is_valid(self):
        return super().is_valid() and self.responsables_valid()

    def responsables_valid(self):
        return Form.is_valid_forms(self.responsables_forms)

    def invalid_messages(self):
        forms = self.responsables_forms
        messages = super().error_messages() + Form.invalid_messages(forms)
        return messages

    @property
    def values(self):
        self.fields['responsables_id'] = self.responsables_created_id() + \
            self.responsables_id
        return self.fields

    def responsables_created_id(self):
        return list(map(
            lambda responsable: responsable.id, self.responsables_saved
        ))
