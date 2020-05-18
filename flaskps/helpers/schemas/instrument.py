from flaskps.models.instrument import Instrument

from .instrument_type import InstrumentTypeSchema

from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from base64 import b64encode


class ImageField(fields.Field):
    """Convert image field to base64 for serialize/deserialize
    """

    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return ""

        return b64encode(value).decode("utf-8")

    def _deserialize(self, value, attr, data, **kwargs):
        return b64encode(value).decode("utf-8")


class InstrumentSchema(SQLAlchemyAutoSchema):

    class Meta:
        model = Instrument

    image = ImageField(attribute="image")
    category = fields.Nested(InstrumentTypeSchema)
