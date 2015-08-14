# -*- coding: utf-8 -*-

from flask_restful import Resource, reqparse, marshal_with
from flask_restful_swagger import swagger
from app.mod_shared.models import db
from app.mod_profiles.models import *
from app.mod_profiles.resources.fields.measurementFields import MeasurementFields

parser = reqparse.RequestParser()
parser.add_argument('datetime', required=True)
parser.add_argument('value', type=float, required=True)
parser.add_argument('profile_id', type=int, required=True)
parser.add_argument('measurement_source_id', type=int)
parser.add_argument('measurement_type_id', type=int, required=True)
parser.add_argument('measurement_unit_id', type=int, required=True)

class MeasurementList(Resource):
    @swagger.operation(
        notes=u'Retorna todas las instancias existentes de medición.'.encode('utf-8'),
        responseClass='MeasurementFields',
        nickname='measurementList_get',
        responseMessages=[
            {
              "code": 200,
              "message": "Solicitud resuelta exitosamente."
            }
          ]
        )
    @marshal_with(MeasurementFields.resource_fields, envelope='resource')
    def get(self):
        measurements = Measurement.query.all()
        return measurements

    @swagger.operation(
        notes=u'Crea una nueva instancia de medición, y la retorna.'.encode('utf-8'),
        responseClass='MeasurementFields',
        nickname='measurementList_post',
        parameters=[
            {
              "name": "id",
              "description": u'Identificador único de la medición.'.encode('utf-8'),
              "required": True,
              "dataType": "int",
              "paramType": "path"
            },
            {
              "name": "datetime",
              "description": u'Fecha y hora de la medición.'.encode('utf-8'),
              "required": True,
              "dataType": "datetime",
              "paramType": "body"
            },
            {
              "name": "value",
              "description": u'Valor de la medición.'.encode('utf-8'),
              "required": True,
              "dataType": "float",
              "paramType": "body"
            },
            {
              "name": "profile_id",
              "description": u'Identificador único del perfil asociado.'.encode('utf-8'),
              "required": True,
              "dataType": "int",
              "paramType": "body"
            },
            {
              "name": "measurement_source_id",
              "description": u'Identificador único de la fuente de medición asociada.'.encode('utf-8'),
              "required": False,
              "dataType": "int",
              "paramType": "body"
            },
            {
              "name": "measurement_type_id",
              "description": u'Identificador único del tipo de medición asociado.'.encode('utf-8'),
              "required": True,
              "dataType": "int",
              "paramType": "body"
            },
            {
              "name": "measurement_unit_id",
              "description": u'Identificador único de la unidad de medición asociada.'.encode('utf-8'),
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
    @marshal_with(MeasurementFields.resource_fields, envelope='resource')
    def post(self):
        args = parser.parse_args()
        new_measurement = Measurement(args['datetime'],
                                      args['value'],
                                      args['profile_id'],
                                      args['measurement_source_id'],
                                      args['measurement_type_id'],
                                      args['measurement_unit_id'])
        db.session.add(new_measurement)
        db.session.commit()
        return new_measurement, 201
