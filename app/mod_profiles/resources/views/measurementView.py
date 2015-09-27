# -*- coding: utf-8 -*-

from flask_restful import Resource, marshal_with
from flask_restful_swagger import swagger

from app.mod_shared.models.db import db
from app.mod_profiles.models import Measurement
from app.mod_profiles.common.fields.measurementFields import MeasurementFields
from app.mod_profiles.common.parsers.measurement import parser_put


class MeasurementView(Resource):
    @swagger.operation(
        notes=u'Retorna una instancia específica de medición.'.encode('utf-8'),
        responseClass='MeasurementFields',
        nickname='measurementView_get',
        parameters=[
            {
              "name": "id",
              "description": u'Identificador único de la medición.'.encode('utf-8'),
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
    @marshal_with(MeasurementFields.resource_fields, envelope='resource')
    def get(self, id):
        measurement = Measurement.query.get_or_404(id)
        return measurement

    @swagger.operation(
        notes=u'Actualiza una instancia específica de medición, y la retorna.'.encode('utf-8'),
        responseClass='MeasurementFields',
        nickname='measurementView_put',
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
    @marshal_with(MeasurementFields.resource_fields, envelope='resource')
    def put(self, id):
        measurement = Measurement.query.get_or_404(id)
        args = parser_put.parse_args()

        # Actualiza los atributos y relaciones del objeto, en base a los
        # argumentos recibidos.

        # Actualiza la fecha y hora, en caso de que haya sido modificada.
        if (args['datetime'] is not None and
              measurement.datetime != args['datetime']):
            measurement.datetime = args['datetime']
        # Actualiza el valor, en caso de que haya sido modificado.
        if (args['value'] is not None and
              measurement.value != args['value']):
            measurement.value = args['value']
        # Actualiza el análisis asociado, en caso de que haya sido modificado.
        if (args['analysis_id'] is not None and
              measurement.analysis_id != args['analysis_id']):
            measurement.analysis_id = args['analysis_id']
        # Actualiza el perfil asociado, en caso de que haya sido modificado.
        if (args['profile_id'] is not None and
              measurement.profile_id != args['profile_id']):
            measurement.profile_id = args['profile_id']
        # Actualiza la fuente de la medicion, en caso de que haya sido
        # modificada.
        if (args['measurement_source_id'] is not None and
              measurement.measurement_source_id != args['measurement_source_id']):
            measurement.measurement_source_id = args['measurement_source_id']
        # Actualiza el tipo de medicion, en caso de que haya sido modificado.
        if (args['measurement_type_id'] is not None and
              measurement.measurement_type_id != args['measurement_type_id']):
            measurement.measurement_type_id = args['measurement_type_id']
        # Actualiza la unidad de medida asociada, en caso de que haya sido
        # modificada.
        if (args['measurement_unit_id'] is not None and
              measurement.measurement_unit_id != args['measurement_unit_id']):
            measurement.measurement_unit_id = args['measurement_unit_id']

        db.session.commit()
        return measurement, 200
