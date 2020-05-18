from flaskps.models.instrument import Instrument

# Routing
from flask_restful import Resource

# Schemas
from flaskps.helpers.schemas.instrument import InstrumentSchema

# Forms
from flaskps.helpers.restful.serializers import InstrumentEditSerializer
from flaskps.helpers.restful.serializers import InstrumentCreateSerializer
from flaskps.helpers.restful.serializers import ImageEditSerializer

from flask import request


class InstrumentRest(Resource):
    def get(self, instrument_id=None):
        schema = InstrumentSchema()

        if instrument_id is None:
            # Index
            instrument = Instrument.all_with_representative_entities()

            return schema.dump(instrument, many=True)

        else:
            # Profile
            instrument = Instrument.query.get(instrument_id)

            return schema.dump(instrument)

    def put(self, instrument_id):
        instrument = Instrument.query.get(instrument_id)
        serializer = InstrumentEditSerializer(request, instrument)

        return serializer.dump()

    def post(self):
        serializer = InstrumentCreateSerializer(request)

        return serializer.dump()


class InstrumentStatusRest(Resource):

    def patch(self, instrument_id):
        instrument = Instrument.query.get(instrument_id)
        status = instrument.switch_status()

        return {
            'message': 'success',
            'status': status
        }


class InstrumentImageRest(Resource):
    def put(self, instrument_id):
        instrument = Instrument.query.get(instrument_id)
        serializer = ImageEditSerializer(request, instrument)

        return serializer.dump()
