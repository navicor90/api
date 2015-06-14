from flask_restful import Resource, reqparse, fields, marshal_with
from app.mod_shared.models import db
from app.mod_profiles.models import *
from .genderView import resource_fields as relation_gender_fields

parser = reqparse.RequestParser()
parser.add_argument('last_name', type=str, required=True)
parser.add_argument('first_name', type=str, required=True)
parser.add_argument('gender_id', type=int)
parser.add_argument('birthday')

resource_fields = {
    'id': fields.Integer,
    'last_name': fields.String,
    'first_name': fields.String,
    'gender': fields.Nested(relation_gender_fields),
    'birthday': fields.DateTime(dt_format='iso8601'),
}

class ProfileView(Resource):
    @marshal_with(resource_fields, envelope='resource')
    def get(self, id):
        profile = Profile.query.get_or_404(id)
        return profile

    @marshal_with(resource_fields, envelope='resource')
    def put(self, id):
        profile = Profile.query.get_or_404(id)
        args = parser.parse_args()

        # Actualiza los atributos y relaciones del objeto, en base a los
        # argumentos recibidos.

        # Actualiza el apellido, en caso de que haya sido modificado.
        if (args['last_name'] is not None and
              profile.last_name != args['last_name']):
            profile.last_name = args['last_name']
        # Actualiza el nombre, en caso de que haya sido modificado.
        if (args['first_name'] is not None and
              profile.first_name != args['first_name']):
            profile.first_name = args['first_name']
        # Actualiza el genero, en caso de que haya sido modificado.
        if (args['gender_id'] is not None and
              profile.gender_id != args['gender_id']):
            profile.gender_id = args['gender_id']
        # Actualiza la fecha de nacimiento, en caso de que haya sido
        # modificada.
        if (args['birthday'] is not None and
              profile.birthday != args['birthday']):
            profile.birthday = args['birthday']

        db.session.commit()
        return profile, 200