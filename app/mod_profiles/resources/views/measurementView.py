# -*- coding: utf-8 -*-

from flask import g
from flask_restful import Resource, marshal_with
from flask_restful_swagger import swagger

from app.mod_shared.models.auth import auth
from app.mod_shared.models.db import db
from app.mod_profiles.models import Measurement
from app.mod_profiles.common.fields.measurementFields import MeasurementFields
from app.mod_profiles.common.parsers.measurement import parser_put
from app.mod_profiles.common.persistence import permission
from app.mod_profiles.common.swagger.responses.generic_responses import code_200_found, code_200_updated, \
    code_204_deleted, code_401, code_403, code_404


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
            code_200_found,
            code_404
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
              "required": False,
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
            code_200_updated,
            code_401,
            code_403,
            code_404
        ]
    )
    @auth.login_required
    @marshal_with(MeasurementFields.resource_fields, envelope='resource')
    def put(self, id):
        measurement = Measurement.query.get_or_404(id)
        args = parser_put.parse_args()

        # Verifica que el usuario autenticado tenga permiso para editar las
        # mediciones del análisis asociado a la medición especificada, en caso
        # de que exista.
        if (measurement.analysis is not None and
                not permission.get_permission_by_user(measurement.analysis, g.user, 'edit_measurements')):
            return '', 403

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
        # Actualiza la fuente de la medición, en caso de que haya sido
        # modificada.
        if (args['measurement_source_id'] is not None and
              measurement.measurement_source_id != args['measurement_source_id']):
            measurement.measurement_source_id = args['measurement_source_id']
        # Actualiza el tipo de medición, en caso de que haya sido modificado.
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

    @swagger.operation(
        notes=u'Elimina una instancia específica de medición.'.encode('utf-8'),
        nickname='measurementView_delete',
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
            code_204_deleted,
            code_401,
            code_403,
            code_404
        ]
    )
    @auth.login_required
    @marshal_with(MeasurementFields.resource_fields, envelope='resource')
    def delete(self, id):
        # Obtiene la medición.
        measurement = Measurement.query.get_or_404(id)

        # Verifica que el usuario autenticado tenga permiso para editar las
        # mediciones del análisis asociado a la medición especificada, en caso
        # de que exista.
        if (measurement.analysis is not None and
                not permission.get_permission_by_user(measurement.analysis, g.user, 'edit_measurements')):
            return '', 403

        # Elimina la medición.
        db.session.delete(measurement)
        db.session.commit()

        return '', 204
