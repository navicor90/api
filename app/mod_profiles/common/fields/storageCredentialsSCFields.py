# -*- coding: utf-8 -*-

from flask_restful import fields

class StorageCredentialsSCFields:
    resource_fields = {
        'id': fields.Integer,
        'token': fields.String,
        'active': fields.Boolean
    }

    required = [
        'id'
    ]
