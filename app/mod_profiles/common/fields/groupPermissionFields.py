# -*- coding: utf-8 -*-

from flask_restful import fields
from flask_restful_swagger import swagger

from .analysisFields import AnalysisFields
from .groupFields import GroupFields


@swagger.model
@swagger.nested(analysis='AnalysisFields',
                group='GroupFields')
class GroupPermissionFields:
    resource_fields = {
        'id': fields.Integer,
        'analysis': fields.Nested(AnalysisFields.resource_fields),
        'group': fields.Nested(GroupFields.resource_fields),
    }

    required = [
        'id',
        'analysis',
        'group',
    ]
