# -*- coding: utf-8 -*-

from flask_restful import Resource, marshal_with
from flask_restful_swagger import swagger
from app.mod_profiles.common.persistence import measurement
from app.mod_profiles.models import Profile
from app.mod_profiles.common.fields.measurementFields import MeasurementFields
from app.mod_profiles.common.parsers.profileMeasurementList import parser_get


class ProfileMeasurementList(Resource):
    # Crea una copia de los campos del recurso 'MeasurementView'.
    resource_fields = MeasurementFields.resource_fields.copy()
    # Quita el perfil asociado de los campos del recurso.
    del resource_fields['profile']

    @swagger.operation(
        notes= (u'Retorna todas las instancias existentes de medición, '
                'asociadas a un perfil específico, ordenadas por fecha y hora '
                'de la medición.').encode('utf-8'),
        responseClass='MeasurementFields',
        nickname='profileMeasurementList_get',
        parameters=[
            {
              "name": "profile_id",
              "description": u'Identificador único del perfil.'.encode('utf-8'),
              "required": True,
              "dataType": "int",
              "paramType": "path"
            },
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
    @marshal_with(resource_fields, envelope='resource')
    def get(self, profile_id):
        # Obtiene el perfil
        profile = Profile.query.get_or_404(profile_id)

        # Obtiene los valores de los argumentos recibidos en la petición.
        args = parser_get.parse_args()
        measurement_source_id = args['source']
        measurement_type_id = args['type']
        measurement_unit_id = args['unit']

        # Obtiene todas las mediciones asociadas al perfil.
        measurements = measurement.get_by_profile(profile = profile,
                                                  source_id = measurement_source_id,
                                                  type_id = measurement_type_id,
                                                  unit_id = measurement_unit_id)
        return measurements
