# -*- coding: utf-8 -*-

from flask_restful import fields
from flask_restful_swagger import swagger

from .analysisFields import AnalysisFields
from .profileFields import ProfileFields


@swagger.model
@swagger.nested(profile='ProfileFields',
                analysis='AnalysisFields')
class AnalysisCommentFields:
    resource_fields = {
        'id': fields.Integer,
        'datetime': fields.DateTime(dt_format='iso8601'),
        'comment': fields.String,
        'analysis': fields.Nested(AnalysisFields.resource_fields),
        'profile': fields.Nested(ProfileFields.resource_fields),
    }

    required = ['id',
                'datetime',
                'comment',
                'analysis',
                'profile',
                ]
