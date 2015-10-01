# -*- coding: utf-8 -*-

from flask_restful import Resource, marshal_with
from flask_restful_swagger import swagger

from app.mod_shared.models.db import db
from app.mod_profiles.models import MeasurementType
from app.mod_profiles.common.fields.measurementTypeFields import MeasurementTypeFields
from app.mod_profiles.common.parsers.measurementType import parser_put
from app.mod_profiles.common.swagger.responses.generic_responses import code_200_found, code_200_updated, code_404


class MeasurementTypeView(Resource):
    @swagger.operation(
        notes=u'Retorna una instancia específica de tipo de medición.'.encode('utf-8'),
        responseClass='MeasurementTypeFields',
        nickname='measurementTypeView_get',
        parameters=[
            {
              "name": "id",
              "description": u'Identificador único del tipo de medición.'.encode('utf-8'),
              "required": True,
              "dataType": "int",
              "paramType": "path"
            }
          ],
        responseMessages=[
            code_200_found,
            code_404
        ]
    )
    @marshal_with(MeasurementTypeFields.resource_fields, envelope='resource')
    def get(self, id):
        measurement_type = MeasurementType.query.get_or_404(id)
        return measurement_type

    @swagger.operation(
        notes=u'Actualiza una instancia específica de tipo de medición, y la retorna.'.encode('utf-8'),
        responseClass='MeasurementTypeFields',
        nickname='measurementTypeView_put',
        parameters=[
            {
              "name": "id",
              "description": u'Identificador único del tipo de medición.'.encode('utf-8'),
              "required": True,
              "dataType": "int",
              "paramType": "path"
            },
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
            code_200_updated,
            code_404
        ]
    )
    @marshal_with(MeasurementTypeFields.resource_fields, envelope='resource')
    def put(self, id):
        measurement_type = MeasurementType.query.get_or_404(id)
        args = parser_put.parse_args()

        # Actualiza los atributos y relaciones del objeto, en base a los
        # argumentos recibidos.

        # Actualiza el nombre, en caso de que haya sido modificado.
        if (args['name'] is not None and
              measurement_type.name != args['name']):
            measurement_type.name = args['name']
        # Actualiza la descripcion, en caso de que haya sido modificada.
        if (args['description'] is not None and
              measurement_type.description != args['description']):
            measurement_type.description = args['description']

        db.session.commit()
        return measurement_type, 200
