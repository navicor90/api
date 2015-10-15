# -*- coding: utf-8 -*-

from flask_restful import fields
from flask_restful_swagger import swagger


@swagger.model
class PermissionTypeFields:
    resource_fields = {
        'id': fields.Integer,
        'name': fields.String,
        'description': fields.String,
        'can_view_analysis_files': fields.Boolean,
        'can_view_measurements': fields.Boolean,
        'can_edit_analysis_files': fields.Boolean,
        'can_edit_measurements': fields.Boolean,
    }

    required = ['id',
                'name',
                'can_view_analysis_files',
                'can_view_measurements',
                'can_edit_analysis_files',
                'can_edit_measurements']
