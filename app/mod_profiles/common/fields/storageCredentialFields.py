# -*- coding: utf-8 -*-

from flask_restful import fields
from flask_restful_swagger import swagger
from .storageLocationFields import StorageLocationFields
from .userFields import UserFields


@swagger.model
@swagger.nested(owner='UserFields',
                storage_location='StorageLocationFields')
class StorageCredentialFields:
    resource_fields = {
        'id': fields.Integer,
        'token': fields.String,
        'owner': fields.Nested(UserFields.resource_fields),
        'storage_location': fields.Nested(StorageLocationFields.resource_fields),
    }

    required = ['id',
                'token',
                'owner',
                'storage_location']
