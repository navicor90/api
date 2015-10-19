# -*- coding: utf-8 -*-

from flask import g
from flask_restful import Resource, marshal_with
from flask_restful_swagger import swagger

from app.mod_shared.models.auth import auth
from app.mod_shared.models.db import db
from app.mod_profiles.common.fields.storageCredentialFields import StorageCredentialFields
from app.mod_profiles.common.parsers.storageCredential import parser_post_auth
from app.mod_profiles.common.swagger.responses.generic_responses import code_200_found, code_201_created, code_401
from app.mod_profiles.models import StorageCredential


class MyStorageCredentialList(Resource):
    # Crea una copia de los campos de 'StorageCredential'.
    resource_fields = StorageCredentialFields.resource_fields.copy()
    # Quita el usuario asociado de la lista de campos.
    del resource_fields['owner']

    @swagger.operation(
        # TODO: Añadir parámetros de autenticación a la documentación Swagger.
        notes=(u'Retorna todas las instancias existentes de credencial de '
               'almacenamiento, asociadas al usuario autenticado.').encode('utf-8'),
        responseClass='StorageCredentialFields',
        nickname='myStorageCredentialList_get',
        responseMessages=[
            code_200_found,
            code_401
        ]
    )
    @auth.login_required
    @marshal_with(resource_fields, envelope='resource')
    def get(self):
        # Obtiene todas las credenciales de almacenamiento asociadas al usuario
        # autenticado.
        storage_credentials = g.user.storage_credentials.all()
        return storage_credentials

    @swagger.operation(
        notes=(u'Crea una nueva instancia de credencial de almacenamiento '
               'asociada al usuario autenticado, y la retorna.').encode('utf-8'),
        responseClass='StorageCredentialFields',
        nickname='myStorageCredentialList_post',
        parameters=[
            {
                "name": "token",
                "description": (u'Token autorizada del usuario, como credencial '
                                'para el servicio de almacenamiento.').encode('utf-8'),
                "required": True,
                "dataType": "string",
                "paramType": "body"
            },
            {
              "name": "storage_location_id",
              "description": (u'Identificador único de la ubicación de '
                              'almacenamiento asociada.').encode('utf-8'),
              "required": True,
              "dataType": "int",
              "paramType": "body"
            }
        ],
        responseMessages=[
            code_201_created,
            code_401
        ]
    )
    @auth.login_required
    @marshal_with(StorageCredentialFields.resource_fields, envelope='resource')
    def post(self):
        # Obtiene los valores de los argumentos recibidos en la petición.
        args = parser_post_auth.parse_args()
        token = args['token']
        storage_location_id = args['storage_location_id']

        # Crea la nueva credencial de almacenamiento, asociada al usuario
        # autenticado.
        new_storage_credential = StorageCredential(token,
                                                   g.user.id,
                                                   storage_location_id)
        db.session.add(new_storage_credential)
        db.session.commit()
        return new_storage_credential, 201
