# -*- coding: utf-8 -*-

from flask_restful import fields
from flask_restful_swagger import swagger
from .genderFields import GenderFields

@swagger.model
@swagger.nested(gender='GenderFields')
class ProfileFields:
    resource_fields = {
        'id': fields.Integer,
        'last_name': fields.String,
        'first_name': fields.String,
        'gender': fields.Nested(GenderFields.resource_fields),
        'birthday': fields.DateTime(dt_format='iso8601'),
    }