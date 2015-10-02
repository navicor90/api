# -*- coding: utf-8 -*-

from flask_restful import Resource, marshal_with
from flask_restful_swagger import swagger

from app.mod_shared.models.db import db
from app.mod_profiles.models import StorageCredential
from app.mod_profiles.common.fields.storageCredentialFields import StorageCredentialFields
from app.mod_profiles.common.parsers.storageCredential import parser_put


class StorageCredentialView(Resource):
    @swagger.operation(
        notes=(u'Retorna una instancia específica de credencial de '
               'almacenamiento.').encode('utf-8'),
        responseClass='StorageCredentialFields',
        nickname='storageCredentialView_get',
        parameters=[
            {
              "name": "id",
              "description": (u'Identificador único de la credencial de '
                              'almacenamiento.').encode('utf-8'),
              "required": True,
              "dataType": "int",
              "paramType": "path"
            }
          ],
        responseMessages=[
            {
              "code": 200,
              "message": "Objeto encontrado."
            },
            {
              "code": 404,
              "message": "Objeto inexistente."
            }
          ]
        )
    @marshal_with(StorageCredentialFields.resource_fields, envelope='resource')
    def get(self, id):
        storage_credential = StorageCredential.query.get_or_404(id)
        return storage_credential

    @swagger.operation(
        notes=(u'Actualiza una instancia específica de credencial de '
               'almacenamiento, y la retorna.').encode('utf-8'),
        responseClass='StorageCredentialFields',
        nickname='storageCredentialView_put',
        parameters=[
            {
              "name": "id",
              "description": (u'Identificador único de la credencial de '
                              'almacenamiento.').encode('utf-8'),
              "required": True,
              "dataType": "int",
              "paramType": "path"
            },
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
              "code": 200,
              "message": "Objeto actualizado exitosamente."
            },
            {
              "code": 404,
              "message": "Objeto inexistente."
            }
          ]
        )
    @marshal_with(StorageCredentialFields.resource_fields, envelope='resource')
    def put(self, id):
        storage_credential = StorageCredential.query.get_or_404(id)
        args = parser_put.parse_args()

        # Actualiza los atributos del objeto, en base a los argumentos
        # recibidos.

        # Actualiza el token, en caso de que haya sido modificado.
        if (args['token'] is not None and
              storage_credential.token != args['token']):
            storage_credential.token = args['token']
        # Actualiza el dueño asociado, en caso de que haya sido modificado.
        if (args['owner_id'] is not None and
              storage_credential.owner_id != args['owner_id']):
            storage_credential.owner_id = args['owner_id']
        # Actualiza la ubicación de almacenamiento asociada, en caso de que
        # haya sido modificada.
        if (args['storage_location_id'] is not None and
              storage_credential.storage_location_id != args['storage_location_id']):
            storage_credential.storage_location_id = args['storage_location_id']

        db.session.commit()
        return storage_credential, 200
