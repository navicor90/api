# -*- coding: utf-8 -*-

from flask_restful import Resource, marshal_with
from flask_restful_swagger import swagger

from app.mod_shared.models.db import db
from app.mod_profiles.models import StorageCredential
from app.mod_profiles.common.fields.storageCredentialFields import StorageCredentialFields
from app.mod_profiles.common.parsers.storageCredential import parser_post


class StorageCredentialList(Resource):
    @swagger.operation(
        notes=(u'Retorna todas las instancias existentes de credenciales de '
               'almacenamiento.').encode('utf-8'),
        responseClass='StorageCredentialFields',
        nickname='storageCredentialList_get',
        responseMessages=[
            {
              "code": 200,
              "message": "Solicitud resuelta exitosamente."
            }
          ]
        )
    @marshal_with(StorageCredentialFields.resource_fields, envelope='resource')
    def get(self):
        storage_credentials = StorageCredential.query.all()
        return storage_credentials

    @swagger.operation(
        notes=(u'Crea una nueva instancia de credencial de almacenamiento, y '
               'la retorna.').encode('utf-8'),
        responseClass='StorageCredentialFields',
        nickname='storageCredentialList_post',
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
              "name": "owner_id",
              "description": u'Identificador único del usuario asociado.'.encode('utf-8'),
              "required": True,
              "dataType": "int",
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
            {
              "code": 201,
              "message": "Objeto creado exitosamente."
            }
          ]
        )
    @marshal_with(StorageCredentialFields.resource_fields, envelope='resource')
    def post(self):
        args = parser_post.parse_args()
        new_storage_credential = StorageCredential(args['token'],
                                                   args['owner_id'],
                                                   args['storage_location_id'])
        db.session.add(new_storage_credential)
        db.session.commit()
        return new_storage_credential, 201
