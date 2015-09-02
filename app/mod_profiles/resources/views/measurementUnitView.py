# -*- coding: utf-8 -*-

from flask_restful import Resource, reqparse, marshal_with
from flask_restful_swagger import swagger
from app.mod_shared.models.db import db
from app.mod_profiles.models import MeasurementUnit
from app.mod_profiles.resources.fields.measurementUnitFields import MeasurementUnitFields
from app.mod_profiles.validators.globalValidator import string_without_int

parser = reqparse.RequestParser()
parser.add_argument('name', type=string_without_int, required=True)
parser.add_argument('symbol', type=strint_without_int, required=True)
parser.add_argument('suffix', type=bool)

class MeasurementUnitView(Resource):
    @swagger.operation(
        notes=u'Retorna una instancia específica de unidad de medición.'.encode('utf-8'),
        responseClass='MeasurementUnitFields',
        nickname='measurementUnitView_get',
        parameters=[
            {
              "name": "id",
              "description": u'Identificador único de la unidad de medición.'.encode('utf-8'),
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
        measurement_unit = MeasurementUnit.query.get_or_404(id)
        return measurement_unit

    @swagger.operation(
        notes=u'Actualiza una instancia específica de unidad de medición, y la retorna.'.encode('utf-8'),
        responseClass='MeasurementUnitFields',
        nickname='measurementUnitView_put',
        parameters=[
            {
              "name": "id",
              "description": u'Identificador único de la unidad de medición.'.encode('utf-8'),
              "required": True,
              "dataType": "int",
              "paramType": "path"
            },
            {
              "name": "name",
              "description": u'Nombre de la unidad de medición.'.encode('utf-8'),
              "required": True,
              "dataType": "string",
              "paramType": "body"
            },
            {
              "name": "symbol",
              "description": u'Símbolo de la unidad de medición.'.encode('utf-8'),
              "required": True,
              "dataType": "string",
              "paramType": "body"
            },
            {
              "name": "suffix",
              "description": (u'Variable booleana que indica si el símbolo de '
                              'la unidad de medición es un sufijo (verdadero) '
                              'o un prefijo (falso) del valor de la medición.').encode('utf-8'),
              "required": False,
              "dataType": "boolean",
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
        measurement_unit = MeasurementUnit.query.get_or_404(id)
        args = parser.parse_args()

        # Actualiza los atributos y relaciones del objeto, en base a los
        # argumentos recibidos.

        # Actualiza el nombre, en caso de que haya sido modificado.
        if (args['name'] is not None and
              measurement_unit.name != args['name']):
            measurement_unit.name = args['name']
        # Actualiza el simbolo de la unidad de medida, en caso de que haya sido
        # modificado.
        if (args['symbol'] is not None and
              measurement_unit.symbol != args['symbol']):
            measurement_unit.symbol = args['symbol']
        # Actualiza el estado del sufijo, en caso de que haya sido modificado.
        if (args['suffix'] is not None and
              measurement_unit.suffix != args['suffix']):
            measurement_unit.suffix = args['suffix']

        db.session.commit()
        return measurement_unit, 200
