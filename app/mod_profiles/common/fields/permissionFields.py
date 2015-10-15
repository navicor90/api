# -*- coding: utf-8 -*-

from flask_restful import fields
from flask_restful_swagger import swagger

from .analysisFields import AnalysisFields
from .permissionTypeFields import PermissionTypeFields
from .userFields import UserFields


@swagger.model
@swagger.nested(analysis='AnalysisFields',
                permission_type='PermissionTypeFields',
                user='UserFields')
class PermissionFields:
    resource_fields = {
        'id': fields.Integer,
        'analysis': fields.Nested(AnalysisFields.resource_fields),
        'permission_type': fields.Nested(PermissionTypeFields.resource_fields),
        'user': fields.Nested(UserFields.resource_fields),
    }

    required = ['id',
                'analysis',
                'permission_type',
                'user']
