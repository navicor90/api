from flask_restful import fields
from flask_restful_swagger import swagger
from .profileFields import ProfileFields

@swagger.model
@swagger.nested(profile='ProfileFields')
class UserFields:
    resource_fields = {
        'id': fields.Integer,
        'username': fields.String,
        'email': fields.String,
        'profile': fields.Nested(ProfileFields.resource_fields),
    }

    required = ['id',
                'username',
                'email',
                'profile']