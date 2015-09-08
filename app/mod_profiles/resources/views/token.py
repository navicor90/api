from flask import g
from flask_restful import Resource, fields, marshal_with
from app.mod_shared.models.auth import auth

resource_fields = {
        'token': fields.String,
        'duration': fields.Integer,
    }

class Token(Resource):
    @auth.login_required
    @marshal_with(resource_fields, envelope='resource')
    def get(self):
        token = g.user.generate_auth_token(600)
        new_token = {'token': token.decode('ascii'), 'duration': 600}
        return new_token