from flaskps.models.instrument_type import InstrumentType

from marshmallow_sqlalchemy import SQLAlchemyAutoSchema


class InstrumentTypeSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = InstrumentType
