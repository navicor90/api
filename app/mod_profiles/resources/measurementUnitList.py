from flask_restful import Resource, reqparse, fields, marshal_with
from app.mod_shared.models import db
from app.mod_profiles.models import *

parser = reqparse.RequestParser()
parser.add_argument('name', type=str)
parser.add_argument('symbol', type=str)
parser.add_argument('suffix', type=bool)

resource_fields = {
    'name': fields.String,
    'symbol': fields.String,
    'suffix': fields.Boolean,
}

class MeasurementUnitList(Resource):
    @marshal_with(resource_fields, envelope='resource')
    def get(self):
        measurement_units = MeasurementUnit.query.all()
        return measurement_units

    @marshal_with(resource_fields, envelope='resource')
    def post(self):
        args = parser.parse_args()
        new_measurement_unit = MeasurementUnit(args['name'],
                                               args['symbol'],
                                               args['suffix'])
        db.session.add(new_measurement_unit)
        db.session.commit()
        return new_measurement_unit, 201
