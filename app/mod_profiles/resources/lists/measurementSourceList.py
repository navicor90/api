# -*- coding: utf-8 -*-

from flask_restful import Resource, marshal_with
from flask_restful_swagger import swagger

from app.mod_shared.models.db import db
from app.mod_profiles.models import MeasurementSource
from app.mod_profiles.common.fields.measurementSourceFields import MeasurementSourceFields
from app.mod_profiles.common.parsers.measurementSource import parser_post
from app.mod_profiles.common.swagger.responses.generic_responses import code_200_ok, code_201_created


class MeasurementSourceList(Resource):
    @swagger.operation(
        notes=u'Retorna todas las instancias existentes de fuente de medición.'.encode('utf-8'),
        responseClass='MeasurementSourceFields',
        nickname='measurementSourceList_get',
        responseMessages=[
            code_200_ok
        ]
    )
    @marshal_with(MeasurementSourceFields.resource_fields, envelope='resource')
    def get(self):
        measurement_sources = MeasurementSource.query.all()
        return measurement_sources

    @swagger.operation(
        notes=u'Crea una nueva instancia de fuente de medición, y la retorna.'.encode('utf-8'),
        responseClass='MeasurementSourceFields',
        nickname='measurementSourceList_post',
        parameters=[
            {
              "name": "name",
              "description": u'Nombre de la fuente de medición.'.encode('utf-8'),
              "required": True,
              "dataType": "string",
              "paramType": "body"
            },
            {
              "name": "description",
              "description": u'Descripción de la fuente de medición.'.encode('utf-8'),
              "required": False,
              "dataType": "string",
              "paramType": "body"
            }
          ],
        responseMessages=[
            code_201_created
        ]
    )
    @marshal_with(MeasurementSourceFields.resource_fields, envelope='resource')
    def post(self):
        args = parser_post.parse_args()
        new_measurement_source = MeasurementSource(args['name'],
                                                   args['description'])
        db.session.add(new_measurement_source)
        db.session.commit()
        return new_measurement_source, 201
