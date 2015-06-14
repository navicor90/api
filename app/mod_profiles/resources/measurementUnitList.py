from flask_restful import Resource, reqparse, marshal_with
from app.mod_shared.models import db
from app.mod_profiles.models import *
from .measurementUnitView import resource_fields

parser = reqparse.RequestParser()
parser.add_argument('name', type=str)
parser.add_argument('symbol', type=str)
parser.add_argument('suffix', type=bool)

class MeasurementUnitList(Resource):
    @marshal_with(resource_fields, envelope='resource')
    def get(self):
        measurement_units = MeasurementUnit.query.all()
        return measurement_units

    def post(self):
        args = parser.parse_args()
        new_measurement_unit = MeasurementUnit(args['name'],
                                               args['symbol'],
                                               args['suffix'])
        db.session.add(new_measurement_unit)
        db.session.commit()
