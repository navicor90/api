from flask_restful import Resource, reqparse, marshal_with
from app.mod_shared.models import db
from app.mod_profiles.models import *
from .measurementView import MeasurementView

parser = reqparse.RequestParser()
parser.add_argument('datetime', required=True)
parser.add_argument('value', type=float, required=True)
parser.add_argument('profile_id', type=int, required=True)
parser.add_argument('measurement_source_id', type=int)
parser.add_argument('measurement_type_id', type=int, required=True)
parser.add_argument('measurement_unit_id', type=int, required=True)

class MeasurementList(Resource):
    @marshal_with(MeasurementView.resource_fields, envelope='resource')
    def get(self):
        measurements = Measurement.query.all()
        return measurements

    @marshal_with(MeasurementView.resource_fields, envelope='resource')
    def post(self):
        args = parser.parse_args()
        new_measurement = Measurement(args['datetime'],
                                      args['value'],
                                      args['profile_id'],
                                      args['measurement_source_id'],
                                      args['measurement_type_id'],
                                      args['measurement_unit_id'])
        db.session.add(new_measurement)
        db.session.commit()
        return new_measurement, 201
