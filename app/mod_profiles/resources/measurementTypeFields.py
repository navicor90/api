# -*- coding: utf-8 -*-

from flask_restful import fields
from flask_restful_swagger import swagger

@swagger.model
class MeasurementTypeFields:
    resource_fields = {
        'id': fields.Integer,
        'name': fields.String,
        'description': fields.String,
    }