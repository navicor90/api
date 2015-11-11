# -*- coding: utf-8 -*-

from flask_restful import fields
from flask_restful_swagger import swagger

from .measurementTypeFields import MeasurementTypeFields
from .measurementUnitFields import MeasurementUnitFields


@swagger.model
@swagger.nested(measurement_type='MeasurementTypeFields',
                measurement_unit='MeasurementUnitFields')
class TypeUnitValidationFields:
    resource_fields = {
        'id': fields.Integer,
        'min_value': fields.Float,
        'max_value': fields.Float,
        'measurement_type': fields.Nested(MeasurementTypeFields.resource_fields),
        'measurement_unit': fields.Nested(MeasurementUnitFields.resource_fields),
    }

    required = [
        'id',
        'min_value',
        'max_value',
        'measurement_type',
        'measurement_unit'
    ]
