# -*- coding: utf-8 -*-

from flask_restful import fields
from flask_restful_swagger import swagger

@swagger.model
class MeasurementUnitFields:
    resource_fields = {
        'id': fields.Integer,
        'name': fields.String,
        'symbol': fields.String,
        'suffix': fields.Boolean,
    }

    required = ['id',
                'name',
                'symbol']