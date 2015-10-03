# -*- coding: utf-8 -*-

from flask_restful import Resource, marshal_with
from flask_restful_swagger import swagger
from app.mod_shared.models.db import db
from app.mod_profiles.models import Measurement
from app.mod_profiles.common.fields.measurementFields import MeasurementFields
from app.mod_profiles.common.parsers.measurement import parser_post
from app.mod_profiles.common.swagger.responses.generic_responses import code_200_ok, code_201_created


class MeasurementList(Resource):
    @swagger.operation(
        notes=u'Retorna todas las instancias existentes de medición.'.encode('utf-8'),
        responseClass='MeasurementFields',
        nickname='measurementList_get',
        responseMessages=[
            code_200_ok
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
              "name": "analysis_id",
              "description": u'Identificador único del análisis asociado.'.encode('utf-8'),
              "required": True,
              "dataType": "int",
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
            code_201_created
        ]
    )
    @marshal_with(MeasurementFields.resource_fields, envelope='resource')
    def post(self):
        args = parser_post.parse_args()
        new_measurement = Measurement(args['datetime'],
                                      args['value'],
                                      args['analysis_id'],
                                      args['profile_id'],
                                      args['measurement_source_id'],
                                      args['measurement_type_id'],
                                      args['measurement_unit_id'])
        db.session.add(new_measurement)
        db.session.commit()
        return new_measurement, 201
