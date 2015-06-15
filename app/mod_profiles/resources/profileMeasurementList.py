# -*- coding: utf-8 -*-

from flask_restful import Resource, marshal_with
from flask_restful_swagger import swagger
from app.mod_shared.models import db
from app.mod_profiles.models import *
from .measurementFields import MeasurementFields

class ProfileMeasurementList(Resource):
    # Crea una copia de los campos del recurso 'MeasurementView'.
    resource_fields = MeasurementFields.resource_fields.copy()
    # Quita el perfil asociado de los campos del recurso.
    del resource_fields['profile']

    @swagger.operation(
        notes= (u'Retorna todas las instancias existentes de medición, '
                'asociadas a un perfil específico.').encode('utf-8'),
        responseClass='MeasurementFields',
        nickname='profileMeasurementList_get',
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
        profile = Profile.query.get_or_404(profile_id)
        measurements = profile.measurements.all()
        return measurements