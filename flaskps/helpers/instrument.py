from .form import Validator, Form

import re

from flask import url_for, render_template
from flaskps.models.instrument import Instrument
from flaskps.models.instrument_type import InstrumentType


class CategoryValidator(Validator):

    def __init__(self, form):
        self.category = form['category_id']

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
        self.extensions = r"([a-zA-Z0-9\s_\\.\-\(\):])+(.jpe?g|.png|.gif|.webp|bmp)$"
        self.image = files['image']
        self.max_size = (2**32) - 1

    def validate(self):
        return self.valid_extension() and self.image_size() < self.max_size

    def valid_extension(self):
        return bool(re.match(self.extensions, self.image.filename))

    def image_size(self):
        self.image.seek(0)
        size = len(self.image.read())
        self.image.seek(0)
        return size

    def message(self):
        return 'Imágen inválida'


class EditInventoryNumberValidator(Validator):

    def __init__(self, form, instrument):
        self.instrument = instrument
        self.number = form['inventory_number']

    def validate(self):
        same_number = self.number == self.instrument.inventory_number
        return same_number or not Instrument.any_inventory_number(self.number)

    def message(self):
        return 'Ya existe un instrumento con ese número de inventario'


class InstrumentForm(Form):

    def __init__(self, request):
        super(InstrumentForm, self).__init__(request.form)
        self.validators.extend([
            CategoryValidator(request.form)
        ])

    def values(self):
        return self.fields


class InstrumentCreateForm(InstrumentForm):

    def __init__(self, request):
        super(InstrumentCreateForm, self).__init__(request)
        self.fields['image'] = request.files['image'].read()
        self.validators.extend([
            InventoryNumberValidator(request.form),
            ImageValidator(request.files)
        ])

    def success_message(self):
        return 'Instrumento creado correctamente'

    def save(self):
        Instrument.create(self.fields)

    def success_url(self):
        return url_for('instrument_index')


class InstrumentEditForm(InstrumentForm):

    def __init__(self, request, instrument):
        super(InstrumentEditForm, self).__init__(request)
        self.instrument = instrument
        self.validators.extend([
            EditInventoryNumberValidator(request.form, instrument)
        ])

    def success_message(self):
        return 'Instrumento modificado correctamente'

    def save(self):
        self.instrument.update(self.fields)

    def success_url(self):
        return url_for('instrument_profile', instrument_id=self.instrument.id)


class ImageEditForm(Form):

    def __init__(self, request, instrument):
        super(ImageEditForm, self).__init__(request.form)
        self.instrument = instrument
        self.fields['image'] = request.files['image'].read()
        self.validators.extend([
            ImageValidator(request.files)
        ])

    def success_message(self):
        return 'Imágen modificada correctamente'

    @property
    def values(self):
        return self.fields

    def save(self):
        self.instrument.update_image(self.values)

    def success_url(self):
        return url_for('instrument_profile', instrument_id=self.instrument.id)
