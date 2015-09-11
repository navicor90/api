# -*- coding: utf-8 -*-

from flask_restful import Resource, reqparse, marshal_with
from flask_restful_swagger import swagger
from app.mod_shared.models.db import db
from app.mod_profiles.models import MeasurementUnit
from app.mod_profiles.resources.fields.measurementUnitFields import MeasurementUnitFields

parser = reqparse.RequestParser()
parser.add_argument('name', type=str, required=True)
parser.add_argument('symbol', type=str, required=True)
parser.add_argument('suffix', type=bool)

class MeasurementUnitList(Resource):
    @swagger.operation(
        notes=u'Retorna todas las instancias existentes de unidad de medición.'.encode('utf-8'),
        responseClass='MeasurementUnitFields',
        nickname='measurementUnitList_get',
        responseMessages=[
            {
              "code": 200,
              "message": "Solicitud resuelta exitosamente."
            }
          ]
        )
    @marshal_with(MeasurementUnitFields.resource_fields, envelope='resource')
    def get(self):
        measurement_units = MeasurementUnit.query.all()
        return measurement_units

    @swagger.operation(
        notes=u'Crea una nueva instancia de unidad de medición, y la retorna.'.encode('utf-8'),
        responseClass='MeasurementUnitFields',
        nickname='measurementUnitList_post',
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
              "code": 201,
              "message": "Objeto creado exitosamente."
            }
          ]
        )
    @marshal_with(MeasurementUnitFields.resource_fields, envelope='resource')
    def post(self):
        args = parser.parse_args()
        new_measurement_unit = MeasurementUnit(args['name'],
                                               args['symbol'],
                                               args['suffix'])
        db.session.add(new_measurement_unit)
        db.session.commit()
        return new_measurement_unit, 201
