from .form import Validator, Form

import os

from flask import url_for, render_template
from flaskps.models.instrument import Instrument
from flaskps.models.instrument_type import InstrumentType


class CategoryValidator(Validator):

    def __init__(self, form):
        self.category = form['category']

    def validate(self):
        return InstrumentType.any(self.category)

    def message(self):
        return 'Elija una categoría válida porfavor'


class InventoryNumberValidator(Validator):

    def __init__(self, form):
        self.number = form['inventory_number']

    def validate(self):
        return not Instrument.any_inventory_number(self.number)

    def message(self):
        return 'Ya existe un instrumento con ese número de inventario'


class ImageValidator(Validator):

    def __init__(self, files):
        self.image = files['image']
        self.max_size = (2**32) - 1

    def validate(self):
        return self.image_size() < self.max_size

    def image_size(self):
        self.image.seek(0)
        size = len(self.image.read())
        self.image.seek(0)
        return size

    def message(self):
        return f'La imágen supera los {self.max_size} bytes.'


class InstrumentCreateForm(Form):

    def __init__(self, request):
        super(InstrumentCreateForm, self).__init__(request.form)
        self.fields['image'] = request.files['image'].read()

        self.validators.extend([
            InventoryNumberValidator(request.form),
            CategoryValidator(request.form),
            ImageValidator(request.files)
        ])

    def success_message(self):
        return 'Instrumento creado correctamente'

    def values(self):
        return self.fields

    def save(self):
        Instrument.create(self.fields)

    def success_url(self):
        return url_for('instrument_index')