from flask_restful import Resource, reqparse, marshal_with
from app.mod_shared.models import db
from app.mod_profiles.models import *
from .measurementSourceView import resource_fields

parser = reqparse.RequestParser()
parser.add_argument('name', type=str)
parser.add_argument('description', type=str)

class MeasurementSourceList(Resource):
    @marshal_with(resource_fields, envelope='resource')
    def get(self):
        measurement_sources = MeasurementSource.query.all()
        return measurement_sources

    def post(self):
        args = parser.parse_args()
        new_measurement_source = MeasurementSource(args['name'],
                                                   args['description'])
        db.session.add(new_measurement_source)
        db.session.commit()
