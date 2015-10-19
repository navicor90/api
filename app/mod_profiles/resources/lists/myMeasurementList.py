# -*- coding: utf-8 -*-

from flask import g
from flask_restful import Resource, marshal_with
from flask_restful_swagger import swagger

from app.mod_shared.models.auth import auth
from app.mod_shared.models.db import db
from app.mod_profiles.common.fields.measurementFields import MeasurementFields
from app.mod_profiles.common.persistence import measurement
from app.mod_profiles.common.parsers.measurement import parser_post_auth
from app.mod_profiles.common.parsers.profileMeasurementList import parser_get
from app.mod_profiles.common.swagger.responses.generic_responses import code_200_found, code_201_created, code_401, \
    code_403
from app.mod_profiles.models import Measurement, Analysis


class MyMeasurementList(Resource):
    # Crea una copia de los campos del recurso 'MeasurementView'.
    resource_fields = MeasurementFields.resource_fields.copy()
    # Quita el perfil asociado de los campos del recurso.
    del resource_fields['profile']

    @swagger.operation(
        # TODO: Añadir parámetros de autenticación a la documentación Swagger.
        notes=(u'Retorna todas las instancias existentes de medición, '
                'asociadas al perfil del usuario autenticado, ordenadas por '
                'fecha y hora de la medición.').encode('utf-8'),
        responseClass='MeasurementFields',
        nickname='myMeasurementList_get',
        parameters=[
            {
              "name": "source",
              "description": (u'Identificador único de la fuente de medición. '
                              'Permite filtrar las mediciones, para sólo '
                              'obtener las asociadas a la fuente de medición '
                              'especificada.').encode('utf-8'),
              "required": False,
              "dataType": "int",
              "paramType": "query"
            },
            {
              "name": "type",
              "description": (u'Identificador único del tipo de medición. '
                              'Permite filtrar las mediciones, para sólo '
                              'obtener las asociadas al tipo de medición '
                              'especificado.').encode('utf-8'),
              "required": False,
              "dataType": "int",
              "paramType": "query"
            },
            {
              "name": "unit",
              "description": (u'Identificador único de la unidad de medición. '
                              'Permite filtrar las mediciones, para sólo '
                              'obtener las asociadas a la unidad de medición '
                              'especificada.').encode('utf-8'),
              "required": False,
              "dataType": "int",
              "paramType": "query"
            }
          ],
        responseMessages=[
            code_200_found,
            code_401
        ]
    )
    @auth.login_required
    @marshal_with(resource_fields, envelope='resource')
    def get(self):
        # Obtiene el perfil.
        profile = g.user.profile

        # Obtiene los valores de los argumentos recibidos en la petición.
        args = parser_get.parse_args()
        measurement_source_id = args['source']
        measurement_type_id = args['type']
        measurement_unit_id = args['unit']

        # Obtiene todas las mediciones asociadas al perfil.
        measurements = measurement.get_by_profile(profile=profile,
                                                  source_id=measurement_source_id,
                                                  type_id=measurement_type_id,
                                                  unit_id=measurement_unit_id)
        return measurements

    @swagger.operation(
        notes=(u'Crea una nueva instancia de medición asociada al usuario '
               'autenticado, y la retorna.').encode('utf-8'),
        responseClass='MeasurementFields',
        nickname='myMeasurementList_post',
        parameters=[
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
            code_201_created,
            code_401,
            code_403
        ]
    )
    @auth.login_required
    @marshal_with(MeasurementFields.resource_fields, envelope='resource')
    def post(self):
        # Obtiene los valores de los argumentos recibidos en la petición.
        args = parser_post_auth.parse_args()
        datetime = args['datetime']
        value = args['value']
        analysis_id = args['analysis_id']
        measurement_source_id = args['measurement_source_id']
        measurement_type_id = args['measurement_type_id']
        measurement_unit_id = args['measurement_unit_id']

        # Obtiene el análisis.
        analysis = Analysis.query.get_or_404(analysis_id)

        # Verifica que el usuario sea el dueño del análisis especificado.
        if g.user.id != analysis.profile.user.first().id:
            return '', 403

        new_measurement = Measurement(datetime,
                                      value,
                                      analysis.id,
                                      g.user.profile.id,
                                      measurement_source_id,
                                      measurement_type_id,
                                      measurement_unit_id)
        db.session.add(new_measurement)
        db.session.commit()
        return new_measurement, 201
