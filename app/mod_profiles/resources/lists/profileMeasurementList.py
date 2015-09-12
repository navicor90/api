# -*- coding: utf-8 -*-

from flask_restful import Resource, reqparse, marshal_with
from flask_restful_swagger import swagger
from app.mod_profiles.models import Measurement, Profile
from app.mod_profiles.resources.fields.measurementFields import MeasurementFields

parser = reqparse.RequestParser()
parser.add_argument('source', type=int)
parser.add_argument('type', type=int)
parser.add_argument('unit', type=int)

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

        args = parser.parse_args()
        measurement_source_id = args['source']
        measurement_type_id = args['type']
        measurement_unit_id = args['unit']

        # Obtiene todas las mediciones asociadas al perfil.
        measurements = profile.measurements

        # Filtra las mediciones por fuente de medición.
        if (measurement_source_id is not None):
            measurements = measurements.filter_by(measurement_source_id=measurement_source_id)
        # Filtra las mediciones por tipo de medición.
        if (measurement_type_id is not None):
            measurements = measurements.filter_by(measurement_type_id=measurement_type_id)
        # Filtra las mediciones por unidad de medición.
        if (measurement_unit_id is not None):
            measurements = measurements.filter_by(measurement_unit_id=measurement_unit_id)

        # Ordena las mediciones por fecha y hora, y las retorna.
        measurements = measurements.order_by(Measurement.datetime).all()
        return measurements