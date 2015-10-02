# -*- coding: utf-8 -*-

from flask_restful import Resource, marshal_with
from flask_restful_swagger import swagger
from app.mod_shared.models.db import db
from app.mod_profiles.models import StorageLocation
from app.mod_profiles.common.fields.storageLocationFields import StorageLocationFields
from app.mod_profiles.common.parsers.storageLocation import parser_post


class StorageLocationList(Resource):
    @swagger.operation(
        notes=(u'Retorna todas las instancias existentes de ubicaciones de '
               'almacenamiento.').encode('utf-8'),
        responseClass='StorageLocationFields',
        nickname='storageLocationList_get',
        responseMessages=[
            {
              "code": 200,
              "message": "Solicitud resuelta exitosamente."
            }
          ]
        )
    @marshal_with(StorageLocationFields.resource_fields, envelope='resource')
    def get(self):
        storage_locations = StorageLocation.query.all()
        return storage_locations

    @swagger.operation(
        notes=(u'Crea una nueva instancia de ubicación de almacenamiento, y la '
               'retorna.').encode('utf-8'),
        responseClass='StorageLocationFields',
        nickname='storageLocationList_post',
        parameters=[
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
              "code": 201,
              "message": "Objeto creado exitosamente."
            }
          ]
        )
    @marshal_with(StorageLocationFields.resource_fields, envelope='resource')
    def post(self):
        args = parser_post.parse_args()
        new_storage_location = StorageLocation(args['name'],
                                               args['description'],
                                               args['website'])
        db.session.add(new_storage_location)
        db.session.commit()
        return new_storage_location, 201
