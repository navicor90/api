from flask_restful import Resource, reqparse, fields, marshal_with
from app.mod_shared.models import db
from app.mod_profiles.models import *

parser = reqparse.RequestParser()
parser.add_argument('name', type=str, required=True)
parser.add_argument('symbol', type=str, required=True)
parser.add_argument('suffix', type=bool)

resource_fields = {
    'name': fields.String,
    'symbol': fields.String,
    'suffix': fields.Boolean,
}

class MeasurementUnitView(Resource):
    @marshal_with(resource_fields, envelope='resource')
    def get(self, id):
        measurement_unit = MeasurementUnit.query.get_or_404(id)
        return measurement_unit

    def put(self, id):
        measurement_unit = MeasurementUnit.query.get_or_404(id)
        args = parser.parse_args()
        measurement_unit.name(args['name'])
        measurement_unit.symbol(args['symbol'])
        measurement_unit.suffix(args['suffix'])
        db.session.commit()
