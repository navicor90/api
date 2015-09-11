# -*- coding: utf-8 -*-

from flask_restful import fields
from flask_restful_swagger import swagger

@swagger.model
class TokenFields:
    resource_fields = {
        'token': fields.String,
        'duration': fields.Integer,
    }