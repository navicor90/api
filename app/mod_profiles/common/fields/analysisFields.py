# -*- coding: utf-8 -*-

from flask_restful import fields
from flask_restful_swagger import swagger

from .profileFields import ProfileFields


@swagger.model
@swagger.nested(profile='ProfileFields')
class AnalysisFields:
    resource_fields = {
        'id': fields.Integer,
        'datetime': fields.DateTime(dt_format='iso8601'),
        'description': fields.String,
        'profile': fields.Nested(ProfileFields.resource_fields),
    }

    required = ['id',
                'datetime',
                'description',
                'profile']
