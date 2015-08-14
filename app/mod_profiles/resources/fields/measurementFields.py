# -*- coding: utf-8 -*-

from flask_restful import fields
from flask_restful_swagger import swagger
from .profileFields import ProfileFields
from .measurementSourceFields import MeasurementSourceFields
from .measurementTypeFields import MeasurementTypeFields
from .measurementUnitFields import MeasurementUnitFields

@swagger.model
@swagger.nested(profile='ProfileFields',
                measurement_source='MeasurementSourceFields',
                measurement_type='MeasurementTypeFields',
                measurement_unit='MeasurementUnitFields')
class MeasurementFields:
    resource_fields = {
        'id': fields.Integer,
        'datetime': fields.DateTime(dt_format='iso8601'),
        'value': fields.Float,
        'profile': fields.Nested(ProfileFields.resource_fields),
        'measurement_source': fields.Nested(MeasurementSourceFields.resource_fields),
        'measurement_type': fields.Nested(MeasurementTypeFields.resource_fields),
        'measurement_unit': fields.Nested(MeasurementUnitFields.resource_fields),
    }

    required = ['id',
                'datetime',
                'value',
                'profile',
                'measurement_type',
                'measurement_unit']