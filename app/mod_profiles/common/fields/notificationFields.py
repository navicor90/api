# -*- coding: utf-8 -*-

from flask_restful import fields
from flask_restful_swagger import swagger

from .profileFields import ProfileFields


@swagger.model
@swagger.nested(notification_owner='ProfileFields')
class NotificationFields:
    resource_fields = {
        'id': fields.Integer,
        'created_datetime': fields.DateTime(dt_format='iso8601'),
        'read_datetime': fields.DateTime(dt_format='iso8601'),
        'notification_owner': fields.Nested(ProfileFields.resource_fields),
        'title': fields.String,
        'description': fields.String,
        'detail_object_type': fields.String,
        'detail_object_id': fields.Integer,
    }

    required = [
        'id',
        'created_datetime',
        'read_datetime',
        'notification_owner',
        'title',
        'description',
        'detail_object_type',
        'detail_object_id',
    ]
