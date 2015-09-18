# -*- coding: utf-8 -*-

from flask_restful import Resource, reqparse, marshal_with
from flask_restful_swagger import swagger
from app.mod_shared.models.db import db
from app.mod_profiles.models import MeasurementType, MeasurementUnit
from app.mod_profiles.resources.fields.measurementUnitFields import MeasurementUnitFields
from app.mod_profiles.common.parsers.measurementTypeUnitsList import parser_put


class MeasurementTypeUnitsList(Resource):
    @swagger.operation(
        notes=(u'Retorna la lista de unidades de medición relacionadas a un '
               'tipo de medición específico.').encode('utf-8'),
        responseClass='MeasurementUnitFields',
        nickname='measurementTypeUnitsList_get',
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
    @marshal_with(MeasurementUnitFields.resource_fields, envelope='resource')
    def get(self, id):
        measurement_type = MeasurementType.query.get_or_404(id)
        measurement_units = measurement_type.measurement_units
        return measurement_units

    @swagger.operation(
        notes=(u'Actualiza la lista de unidades de medición asociadas a una '
               'instancia específica de tipo de medición, y la retorna.').encode('utf-8'),
        responseClass='MeasurementUnitFields',
        nickname='measurementTypeUnitsList_put',
        parameters=[
            {
              "name": "id",
              "description": u'Identificador único del tipo de medición.'.encode('utf-8'),
              "required": True,
              "dataType": "int",
              "paramType": "path"
            },
            {
              "name": "measurement_unit_id_list",
              "description": (u'Lista de identificadores únicos de las unidades '
                              'de medición.').encode('utf-8'),
              "required": True,
              "dataType": "list",
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
    @marshal_with(MeasurementUnitFields.resource_fields, envelope='resource')
    def put(self, id):
        measurement_type = MeasurementType.query.get_or_404(id)
        args = parser_put.parse_args()

        # Actualiza la relación de tipo de medición con unidades de medición,
        # en base a los argumentos recibidos.

        # Elimina los elementos duplicados de la lista de identificadores de
        # unidades de medición.
        new_units_id_list = list(set(args['measurement_unit_id_list']))

        # Recorre las unidades de medición actualmente asociadas al tipo de
        # medición.
        for measurement_unit in measurement_type.measurement_units:
            # Si el identificador de la unidad de medición se encuentra en la
            # lista de identificadores especificada, se quita de la misma.
            if (measurement_unit.id in new_units_id_list):
                new_units_id_list.remove(measurement_unit.id)
            # Sino, se elimina la relación existente entre el tipo de medición
            # y la unidad de medición.
            else:
                measurement_type.measurement_units.remove(measurement_unit)

        # Recorre los identificadores aún presentes en la lista de
        # identificadores.
        for new_unit_id in new_units_id_list:
            # Obtiene la unidad de medición correspondiente al identificador.
            measurement_unit = MeasurementUnit.query.get(new_unit_id)
            # Si encuentra una unidad de medición para el identificador, crea
            # la relación entre la misma y el tipo de medición.
            if (measurement_unit is not None):
                measurement_type.measurement_units.append(measurement_unit)

        db.session.commit()

        # Retorna todas las unidades de medición asociadas al tipo de medición.
        measurement_units = measurement_type.measurement_units
        return measurement_units, 200
