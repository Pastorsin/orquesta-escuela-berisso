from .form import Validator, Form
from datetime import date, datetime


class DateValidator(Validator):

    def __init__(self, start_date, end_date):
        self.starting_date = start_date
        self.ending_date = end_date

    def validate(self):
        return datetime.strptime(self.starting_date, '%Y-%m-%d').date() < datetime.strptime(self.ending_date, '%Y-%m-%d').date() and datetime.strptime(self.starting_date, '%Y-%m-%d').date() >= date.today()

    def message(self):
        return 'Error! El rango de fechas es inválido!'


class SchoolYearForm(Form):

    def __init__(self, form):
        super(SchoolYearForm, self).__init__(form)

    @property
    def values(self):
        values = self.fields.copy()
        return values


class SchoolYearCreateForm(SchoolYearForm):

    def __init__(self, form):
        super(SchoolYearCreateForm, self).__init__(form)

        self.validators.extend([
            DateValidator(self.fields['starting_date'], self.fields['ending_date'])
        ])

    def success_message(self):
        return 'Ciclo lectivo creado con éxito.'
