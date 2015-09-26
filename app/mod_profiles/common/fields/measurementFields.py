# -*- coding: utf-8 -*-

from flask_restful import fields
from flask_restful_swagger import swagger
from .analysisFields import AnalysisFields
from .measurementSourceFields import MeasurementSourceFields
from .measurementTypeFields import MeasurementTypeFields
from .measurementUnitFields import MeasurementUnitFields
from .profileFields import ProfileFields


@swagger.model
@swagger.nested(analysis='AnalysisFields',
                profile='ProfileFields',
                measurement_source='MeasurementSourceFields',
                measurement_type='MeasurementTypeFields',
                measurement_unit='MeasurementUnitFields')
class MeasurementFields:
    resource_fields = {
        'id': fields.Integer,
        'datetime': fields.DateTime(dt_format='iso8601'),
        'value': fields.Float,
        'analysis': fields.Nested(AnalysisFields.resource_fields),
        'profile': fields.Nested(ProfileFields.resource_fields),
        'measurement_source': fields.Nested(MeasurementSourceFields.resource_fields),
        'measurement_type': fields.Nested(MeasurementTypeFields.resource_fields),
        'measurement_unit': fields.Nested(MeasurementUnitFields.resource_fields),
    }

    required = ['id',
                'datetime',
                'value',
                'analysis',
                'profile',
                'measurement_type',
                'measurement_unit']
