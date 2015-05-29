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

class ProfileList(Resource):
    @marshal_with(resource_fields, envelope='resource')
    def get(self):
        profiles = Profile.query.all()
        return profiles

    def post(self):
        args = parser.parse_args()
        new_profile = Profile(args['last_name'],
                              args['first_name'],
                              args['gender'],
                              args['birthday'])
        db.session.add(new_profile)
        db.session.commit()
        pass
