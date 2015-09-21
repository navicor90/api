# -*- coding: utf-8 -*-

from flask_restful import Resource, marshal_with
from flask_restful_swagger import swagger
from app.mod_profiles.common.persistence import measurement
from app.mod_profiles.models import Profile
from app.mod_profiles.common.fields.measurementFields import MeasurementFields


class ProfileLatestMeasurementList(Resource):
    # Crea una copia de los campos del recurso 'MeasurementView'.
    resource_fields = MeasurementFields.resource_fields.copy()
    # Quita el perfil asociado de los campos del recurso.
    del resource_fields['profile']

    @swagger.operation(
        notes= (u'Retorna la última instancia de medición de cada tipo de '
                'medición, asociadas a un perfil específico.').encode('utf-8'),
        responseClass='MeasurementFields',
        nickname='profileLatestMeasurementList_get',
        parameters=[
            {
              "name": "profile_id",
              "description": u'Identificador único del perfil.'.encode('utf-8'),
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
    @marshal_with(resource_fields, envelope='resource')
    def get(self, profile_id):
        # Obtiene el perfil.
        profile = Profile.query.get_or_404(profile_id)

        # Obtiene las últimas mediciones asociadas al perfil.
        latest_measurements = measurement.get_latest_by_profile(profile)
        return latest_measurements