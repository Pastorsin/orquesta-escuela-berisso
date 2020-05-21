# Forms
from flaskps.helpers.instrument import InstrumentCreateForm
from flaskps.helpers.instrument import InstrumentEditForm
from flaskps.helpers.instrument import ImageEditForm

# Schemas
from flaskps.helpers.schemas.instrument import InstrumentSchema

from flask import jsonify


class InstrumentSerializer():
    """Adapter of InstrumentForm"""

    schema = InstrumentSchema()

    def __init__(self, *args):
        self.form = self.form(*args)

    def dump(self):
        if self.form.is_valid():
            instrument = self.form.save()
            message = {
                'success': True,
                'messages': [self.form.success_message()],
                'object': self.schema.dump(instrument)
            }
        else:
            message = {
                'success': False,
                'messages': self.form.error_messages(),
                'object': None
            }

        return jsonify(message)


class InstrumentCreateSerializer(InstrumentSerializer):
    form = InstrumentCreateForm


class InstrumentEditSerializer(InstrumentSerializer):
    form = InstrumentEditForm


class ImageEditSerializer(InstrumentSerializer):
    form = ImageEditForm
