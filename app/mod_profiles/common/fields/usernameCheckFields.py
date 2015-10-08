# -*- coding: utf-8 -*-

from flask_restful import fields
from flask_restful_swagger import swagger


@swagger.model
class UsernameCheckFields:
    resource_fields = {
        'available_username': fields.Boolean,
    }
