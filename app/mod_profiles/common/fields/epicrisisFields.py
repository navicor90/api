# -*- coding: utf-8 -*-

from flask_restful import fields


class EpicrisisFields:
    resource_fields = {
        'id': fields.Integer,
        'image_name': fields.String,
        'datetime': fields.DateTime(dt_format='iso8601')
    }

    required = [
        'id'
    ]
