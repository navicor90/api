from flask_restful import Resource, reqparse, fields, marshal_with
from app.mod_shared.models import db
from app.mod_profiles.models import *

parser = reqparse.RequestParser()
parser.add_argument('last_name', type=str)
parser.add_argument('first_name', type=str)
parser.add_argument('gender', type=int)
parser.add_argument('birthday')

resource_fields = {
    'last_name': fields.String,
    'first_name': fields.String,
    'gender': fields.Integer,
    'birthday': fields.DateTime,
}

class ProfileView(Resource):
    @marshal_with(resource_fields, envelope='resource')
    def get(self, id):
        profile = Profile.query.get_or_404(id)
        return profile
