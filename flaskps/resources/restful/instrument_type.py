# Models
from flaskps.models.instrument_type import InstrumentType

# Routing
from flask_restful import Resource

# Schemas
from flaskps.helpers.schemas.instrument_type import InstrumentTypeSchema

# Constraints
from flaskps.helpers.restful.constraints import auth_required
from flaskps.helpers.restful.constraints import permissions_enabled


class InstrumentTypeRest(Resource):

    @auth_required
    @permissions_enabled('instrument_index')
    def get(self):
        schema = InstrumentTypeSchema()

        instrument_types = InstrumentType.query.all()

        return schema.dump(instrument_types, many=True)
