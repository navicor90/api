# -*- coding: utf-8 -*-

from flask_restful import fields
from flask_restful_swagger import swagger

from .analysisFields import AnalysisFields
from .storageLocationFields import StorageLocationFields


@swagger.model
@swagger.nested(analysis='AnalysisFields',
                storage_location='StorageLocationFields')
class AnalysisFileFields:
    resource_fields = {
        'id': fields.Integer,
        'upload_time': fields.DateTime(dt_format='iso8601'),
        'path': fields.String,
        'description': fields.String,
        'analysis': fields.Nested(AnalysisFields.resource_fields),
        'storage_location': fields.Nested(StorageLocationFields.resource_fields),
    }

    required = ['id',
                'path',
                'analysis',
                'storage_location']
