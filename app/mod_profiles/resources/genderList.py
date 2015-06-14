from flask_restful import Resource, reqparse, marshal_with
from app.mod_shared.models import db
from app.mod_profiles.models import *
from .genderView import resource_fields

parser = reqparse.RequestParser()
parser.add_argument('name', type=str, required=True)
parser.add_argument('description', type=str)

class GenderList(Resource):
    @marshal_with(resource_fields, envelope='resource')
    def get(self):
        genders = Gender.query.all()
        return genders

    @marshal_with(resource_fields, envelope='resource')
    def post(self):
        args = parser.parse_args()
        new_gender = Gender(args['name'],
                            args['description'])
        db.session.add(new_gender)
        db.session.commit()
        return new_gender, 201
