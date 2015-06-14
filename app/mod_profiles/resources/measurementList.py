from flask_restful import Resource, reqparse, marshal_with
from app.mod_shared.models import db
from app.mod_profiles.models import *
from .measurementView import resource_fields

parser = reqparse.RequestParser()
parser.add_argument('datetime')
parser.add_argument('value', type=float)
parser.add_argument('profile_id', type=int)
parser.add_argument('measurement_source_id', type=int)
parser.add_argument('measurement_type_id', type=int)
parser.add_argument('measurement_unit_id', type=int)

class MeasurementList(Resource):
    @marshal_with(resource_fields, envelope='resource')
    def get(self):
        measurements = Measurement.query.all()
        return measurements

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
