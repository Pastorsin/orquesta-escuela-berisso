from .form import Validator, Form

import re

from flask import url_for
from flaskps.models.instrument import Instrument
from flaskps.models.instrument_type import InstrumentType

##################################################
# Validators
##################################################


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


class EditInventoryNumberValidator(InventoryNumberValidator):

    def __init__(self, form, instrument):
        super(EditInventoryNumberValidator, self).__init__(form)
        self.instrument = instrument

    def validate(self):
        return self.same_number() or super().validate()

    def same_number(self):
        return self.number == self.instrument.inventory_number


class ImageValidator(Validator):

    def __init__(self, files):
        self.extensions = r"([a-zA-Z0-9\s_\\.\-\(\):])+(.jpe?g|.png|.gif|.webp|bmp)$"
        self.image = files['image']
        self.MAX_SIZE = (2**32) - 1

    def validate(self):
        return self.valid_extension() and self.valid_size()

    def valid_size(self):
        return self.image_size() < self.MAX_SIZE

    def valid_extension(self):
        return bool(re.match(self.extensions, self.image.filename))

    def image_size(self):
        self.image.seek(0)
        size = len(self.image.read())
        self.image.seek(0)
        return size

    def message(self):
        return 'Imágen inválida'


class PositiveInventoryNumberValidator(Validator):

    def __init__(self, form):
        self.number = int(form['inventory_number'])

    def validate(self):
        return self.number > 0

    def message(self):
        return 'El número de inventario debe ser mayor a 0'

##################################################
# Forms
##################################################


class InstrumentForm(Form):

    def __init__(self, request):
        super(InstrumentForm, self).__init__(request.form)
        self.validators.extend([
            CategoryValidator(request.form),
            PositiveInventoryNumberValidator(request.form)
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
            EditInventoryNumberValidator(request.form, instrument),
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
