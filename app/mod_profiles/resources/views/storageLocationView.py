# -*- coding: utf-8 -*-

from flask_restful import Resource, marshal_with
from flask_restful_swagger import swagger

from app.mod_shared.models.db import db
from app.mod_profiles.models import StorageLocation
from app.mod_profiles.common.fields.storageLocationFields import StorageLocationFields
from app.mod_profiles.common.parsers.storageLocation import parser_put


class StorageLocationView(Resource):
    @swagger.operation(
        notes=(u'Retorna una instancia específica de ubicación de '
               'almacenamiento.').encode('utf-8'),
        responseClass='StorageLocationFields',
        nickname='storageLocationView_get',
        parameters=[
            {
              "name": "id",
              "description": (u'Identificador único de la ubicación de '
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
    @marshal_with(StorageLocationFields.resource_fields, envelope='resource')
    def get(self, id):
        storage_location = StorageLocation.query.get_or_404(id)
        return storage_location

    @swagger.operation(
        notes=(u'Actualiza una instancia específica de ubicación de '
               'almacenamiento, y la retorna.').encode('utf-8'),
        responseClass='StorageLocationFields',
        nickname='storageLocationView_put',
        parameters=[
            {
              "name": "id",
              "description": (u'Identificador único de la ubicación de '
                              'almacenamiento.').encode('utf-8'),
              "required": True,
              "dataType": "int",
              "paramType": "path"
            },
            {
              "name": "name",
              "description": u'Nombre de la ubicación de almacenamiento.'.encode('utf-8'),
              "required": True,
              "dataType": "string",
              "paramType": "body"
            },
            {
              "name": "description",
              "description": u'Descripción de la ubicación de almacenamiento.'.encode('utf-8'),
              "required": False,
              "dataType": "string",
              "paramType": "body"
            },
            {
              "name": "website",
              "description": u'Sitio web de la ubicación de almacenamiento.'.encode('utf-8'),
              "required": True,
              "dataType": "string",
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
    @marshal_with(StorageLocationFields.resource_fields, envelope='resource')
    def put(self, id):
        storage_location = StorageLocation.query.get_or_404(id)
        args = parser_put.parse_args()

        # Actualiza los atributos del objeto, en base a los argumentos
        # recibidos.

        # Actualiza el nombre, en caso de que haya sido modificado.
        if (args['name'] is not None and
              storage_location.name != args['name']):
            storage_location.name = args['name']
        # Actualiza la descripción, en caso de que haya sido modificada.
        if (args['description'] is not None and
              storage_location.description != args['description']):
            storage_location.description = args['description']
        # Actualiza el sitio web de la ubicación de almacenamiento, en caso de
        # que haya sido modificado.
        if (args['website'] is not None and
              storage_location.website != args['website']):
            storage_location.website = args['website']

        db.session.commit()
        return storage_location, 200
