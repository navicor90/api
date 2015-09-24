# -*- coding: utf-8 -*-

from flask_restful import Resource, marshal_with
from flask_restful_swagger import swagger
from app.mod_shared.models.db import db
from app.mod_profiles.models import MeasurementType
from app.mod_profiles.common.fields.measurementTypeFields import MeasurementTypeFields
from app.mod_profiles.common.parsers.measurementType import parser_post


class MeasurementTypeList(Resource):
    @swagger.operation(
        notes=u'Retorna todas las instancias existentes de tipo de medición.'.encode('utf-8'),
        responseClass='MeasurementTypeFields',
        nickname='measurementTypeList_get',
        responseMessages=[
            {
              "code": 200,
              "message": "Solicitud resuelta exitosamente."
            }
          ]
        )
    @marshal_with(MeasurementTypeFields.resource_fields, envelope='resource')
    def get(self):
        measurement_types = MeasurementType.query.all()
        return measurement_types

    @swagger.operation(
        notes=u'Crea una nueva instancia de tipo de medición, y la retorna.'.encode('utf-8'),
        responseClass='MeasurementTypeFields',
        nickname='measurementTypeList_post',
        parameters=[
            {
              "name": "name",
              "description": u'Nombre del tipo de medición.'.encode('utf-8'),
              "required": True,
              "dataType": "string",
              "paramType": "body"
            },
            {
              "name": "description",
              "description": u'Descripción del tipo de medición.'.encode('utf-8'),
              "required": False,
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
    @marshal_with(MeasurementTypeFields.resource_fields, envelope='resource')
    def post(self):
        args = parser_post.parse_args()
        new_measurement_type = MeasurementType(args['name'],
                                               args['description'])
        db.session.add(new_measurement_type)
        db.session.commit()
        return new_measurement_type, 201
