# -*- coding: utf-8 -*-

from flask_restful import fields
from flask_restful_swagger import swagger


@swagger.model
class MeasurementSourceFields:
    resource_fields = {
        'id': fields.Integer,
        'name': fields.String,
        'description': fields.String,
    }

    required = ['id',
                'name']
