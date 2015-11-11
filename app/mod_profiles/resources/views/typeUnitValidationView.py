# -*- coding: utf-8 -*-

from flask_restful import Resource, marshal_with
from flask_restful_swagger import swagger

from app.mod_shared.models.db import db
from app.mod_profiles.models import TypeUnitValidation
from app.mod_profiles.common.fields.typeUnitValidationFields import TypeUnitValidationFields
from app.mod_profiles.common.parsers.typeUnitValidation import parser_put
from app.mod_profiles.common.swagger.responses.generic_responses import code_200_found, code_200_updated, \
    code_204_deleted, code_404


class TypeUnitValidationView(Resource):
    @swagger.operation(
        notes=(u'Retorna una instancia específica de validación de unidad de '
               'medición.').encode('utf-8'),
        responseClass='TypeUnitValidationFields',
        nickname='typeUnitValidationView_get',
        parameters=[
            {
                "name": "type_unit_validation_id",
                "description": (u'Identificador único de la validación de '
                                'unidad de medición.').encode('utf-8'),
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
    @marshal_with(TypeUnitValidationFields.resource_fields, envelope='resource')
    def get(self, type_unit_validation_id):
        # Obtiene la validación de unidad de medición.
        type_unit_validation = TypeUnitValidation.query.get_or_404(type_unit_validation_id)
        return type_unit_validation

    @swagger.operation(
        notes=(u'Actualiza una instancia específica de validación de unidad de '
               'medición, y la retorna.').encode('utf-8'),
        responseClass='TypeUnitValidationFields',
        nickname='typeUnitValidationView_put',
        parameters=[
            {
                "name": "type_unit_validation_id",
                "description": (u'Identificador único de la validación de '
                                'unidad de medición.').encode('utf-8'),
                "required": True,
                "dataType": "int",
                "paramType": "path"
            },
            {
                "name": "min_value",
                "description": u'Valor mínimo de la validación.'.encode('utf-8'),
                "required": True,
                "dataType": "float",
                "paramType": "body"
            },
            {
                "name": "max_value",
                "description": u'Valor máximo de la validación.'.encode('utf-8'),
                "required": True,
                "dataType": "float",
                "paramType": "body"
            },
            {
                "name": "measurement_type_id",
                "description": u'Identificador único del tipo de medición.'.encode('utf-8'),
                "required": True,
                "dataType": "int",
                "paramType": "body"
            },
            {
                "name": "measurement_unit_id",
                "description": u'Identificador único de la unidad de medición.'.encode('utf-8'),
                "required": True,
                "dataType": "int",
                "paramType": "body"
            },
        ],
        responseMessages=[
            code_200_updated,
            code_404
        ]
    )
    @marshal_with(TypeUnitValidationFields.resource_fields, envelope='resource')
    def put(self, type_unit_validation_id):
        # Obtiene la validación de unidad de medición.
        type_unit_validation = TypeUnitValidation.query.get_or_404(type_unit_validation_id)

        # Obtiene los valores de los argumentos recibidos en la petición.
        args = parser_put.parse_args()
        min_value = args['min_value']
        max_value = args['max_value']
        measurement_type_id = args['measurement_type_id']
        measurement_unit_id = args['measurement_unit_id']

        # Actualiza los atributos y relaciones del objeto, en base a los
        # argumentos recibidos.

        # Actualiza el valor mínimo, en caso de que haya sido modificado.
        if (min_value is not None and
                type_unit_validation.min_value != min_value):
            type_unit_validation.min_value = min_value
        # Actualiza el valor máximo, en caso de que haya sido modificado.
        if (max_value is not None and
                type_unit_validation.max_value != max_value):
            type_unit_validation.max_value = max_value
        # Actualiza el tipo de medición asociado, en caso de que haya sido
        # modificado.
        if (measurement_type_id is not None and
                type_unit_validation.measurement_type_id != measurement_type_id):
            type_unit_validation.measurement_type_id = measurement_type_id
        # Actualiza la unidad de medición asociada, en caso de que haya sido
        # modificada.
        if (measurement_unit_id is not None and
                type_unit_validation.measurement_unit_id != measurement_unit_id):
            type_unit_validation.measurement_unit_id = measurement_unit_id

        db.session.commit()
        return type_unit_validation, 200

    @swagger.operation(
        notes=(u'Elimina una instancia específica de validación de unidad de '
               'medición.').encode('utf-8'),
        nickname='typeUnitValidationView_delete',
        parameters=[
            {
                "name": "type_unit_validation_id",
                "description": (u'Identificador único de la validación de '
                                'unidad de medición.').encode('utf-8'),
                "required": True,
                "dataType": "int",
                "paramType": "path"
            }
        ],
        responseMessages=[
            code_204_deleted,
            code_404
        ]
    )
    @marshal_with(TypeUnitValidationFields.resource_fields, envelope='resource')
    def delete(self, type_unit_validation_id):
        # Obtiene la validación de unidad de medición.
        type_unit_validation = TypeUnitValidation.query.get_or_404(type_unit_validation_id)

        # Elimina la validación de unidad de medición.
        db.session.delete(type_unit_validation)
        db.session.commit()

        return '', 204
