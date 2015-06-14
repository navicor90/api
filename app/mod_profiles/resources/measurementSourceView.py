from flask_restful import Resource, reqparse, fields, marshal_with
from app.mod_shared.models import db
from app.mod_profiles.models import *

parser = reqparse.RequestParser()
parser.add_argument('name', type=str, required=True)
parser.add_argument('description', type=str)

resource_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'description': fields.String,
}

class MeasurementSourceView(Resource):
    @marshal_with(resource_fields, envelope='resource')
    def get(self, id):
        measurement_source = MeasurementSource.query.get_or_404(id)
        return measurement_source

    @marshal_with(resource_fields, envelope='resource')
    def put(self, id):
        measurement_source = MeasurementSource.query.get_or_404(id)
        args = parser.parse_args()
        measurement_source.name(args['name'])
        measurement_source.description(args['description'])
        db.session.commit()
        return measurement_source, 200