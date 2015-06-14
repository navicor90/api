from flask_restful import Resource, reqparse, marshal_with
from app.mod_shared.models import db
from app.mod_profiles.models import *
from .profileView import resource_fields

parser = reqparse.RequestParser()
parser.add_argument('last_name', type=str, required=True)
parser.add_argument('first_name', type=str, required=True)
parser.add_argument('gender', type=int)
parser.add_argument('birthday')

class ProfileList(Resource):
    @marshal_with(resource_fields, envelope='resource')
    def get(self):
        profiles = Profile.query.all()
        return profiles

    @marshal_with(resource_fields, envelope='resource')
    def post(self):
        args = parser.parse_args()
        new_profile = Profile(args['last_name'],
                              args['first_name'],
                              args['gender'],
                              args['birthday'])
        db.session.add(new_profile)
        db.session.commit()
        return new_profile, 201
