from flaskps.helpers.instrument import InstrumentCreateForm
from flaskps.helpers.instrument import InstrumentEditForm
from flaskps.helpers.instrument import ImageEditForm

from flask import jsonify


class InstrumentSerializer():
    def __init__(self, *args):
        self.form = self.form(*args)

    def dump(self):
        if self.form.is_valid():
            self.form.save()
            message = {
                'success': True,
                'messages': [self.form.success_message()]
            }
        else:
            message = {
                'success': False,
                'messages': self.form.error_messages()
            }

        return jsonify(message)


class InstrumentCreateSerializer(InstrumentSerializer):
    form = InstrumentCreateForm


class InstrumentEditSerializer(InstrumentSerializer):
    form = InstrumentEditForm


class ImageEditSerializer(InstrumentSerializer):
    form = ImageEditForm
