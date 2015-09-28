# -*- coding: utf-8 -*-

from flask_restful import Resource, marshal_with
from app.mod_profiles.resources.fields.storageCredentialsSCFields import StorageCredentialsSCFields

class StorageCredentialsSCView(Resource):
    @marshal_with(StorageCredentialsSCFields.resource_fields, envelope='resource')
    def get(self):
        pass
