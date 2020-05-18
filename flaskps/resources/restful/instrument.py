from flask import request

# Models
from flaskps.models.instrument import Instrument

# Routing
from flask_restful import Resource

# Schemas
from flaskps.helpers.schemas.instrument import InstrumentSchema

# Constraints
from flaskps.helpers.restful.constraints import auth_required
from flaskps.helpers.restful.constraints import permissions_enabled

# Serializers
from flaskps.helpers.restful.serializers import InstrumentEditSerializer
from flaskps.helpers.restful.serializers import InstrumentCreateSerializer
from flaskps.helpers.restful.serializers import ImageEditSerializer


class InstrumentRest(Resource):

    @auth_required
    @permissions_enabled('instrument_index')
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

    @auth_required
    @permissions_enabled('instrument_update')
    def put(self, instrument_id):
        instrument = Instrument.query.get(instrument_id)
        serializer = InstrumentEditSerializer(request, instrument)

        return serializer.dump()

    @auth_required
    @permissions_enabled('instrument_new')
    def post(self):
        serializer = InstrumentCreateSerializer(request)

        return serializer.dump()


class InstrumentStatusRest(Resource):

    @auth_required
    @permissions_enabled('instrument_deactivate')
    @permissions_enabled('instrument_activate')
    def patch(self, instrument_id):
        instrument = Instrument.query.get(instrument_id)
        status = instrument.switch_status()

        return {
            'success': True,
            'status': status
        }


class InstrumentImageRest(Resource):

    @auth_required
    @permissions_enabled('instrument_update')
    def put(self, instrument_id):
        instrument = Instrument.query.get(instrument_id)
        serializer = ImageEditSerializer(request, instrument)

        return serializer.dump()
