# -*- coding: utf-8 -*-

from flask_restful import Resource, marshal_with
from flask_restful_swagger import swagger
from app.mod_shared.models import db
from app.mod_profiles.models import *
from app.mod_profiles.resources.fields.measurementFields import MeasurementFields

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
        measurement_types = MeasurementType.query.all()
        profile = Profile.query.get_or_404(profile_id)
        measurements = profile.measurements
        latest_measurements = []

        for measurement_type in measurement_types:
            latest_from_type = None
            corresponding_measurements = measurements.filter_by(measurement_type_id = measurement_type.id)
            for measurement in corresponding_measurements:
                if (not latest_from_type or
                      measurement.datetime > latest_from_type.datetime):
                    latest_from_type = measurement
            if (latest_from_type):
                latest_measurements.append(latest_from_type)

        return latest_measurements