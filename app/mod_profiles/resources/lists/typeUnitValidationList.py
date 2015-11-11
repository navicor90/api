# -*- coding: utf-8 -*-

from flask_restful import Resource, marshal_with
from flask_restful_swagger import swagger

from app.mod_shared.models.db import db
from app.mod_profiles.models import MeasurementType, MeasurementUnit, TypeUnitValidation
from app.mod_profiles.common.fields.typeUnitValidationFields import TypeUnitValidationFields
from app.mod_profiles.common.parsers.typeUnitValidation import parser_post
from app.mod_profiles.common.swagger.responses.generic_responses import code_200_found, code_201_created, code_404


class TypeUnitValidationList(Resource):
    # Crea una copia de los campos de 'TypeUnitValidation'.
    resource_fields = TypeUnitValidationFields.resource_fields.copy()
    # Quita el tipo de medición asociado, de los campos.
    del resource_fields['measurement_type']

    @swagger.operation(
        notes=(u'Retorna la lista de validaciones de unidad de medición, '
               'relacionadas a un tipo de medición específico.').encode('utf-8'),
        responseClass='TypeUnitValidationFields',
        nickname='typeUnitValidationList_get',
        parameters=[
            {
                "name": "measurement_type_id",
                "description": u'Identificador único del tipo de medición.'.encode('utf-8'),
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
    @marshal_with(resource_fields, envelope='resource')
    def get(self, measurement_type_id):
        # Obtiene el tipo de medición.
        measurement_type = MeasurementType.query.get_or_404(measurement_type_id)

        # Obtiene las validaciones de unidad de medición asociadas al tipo de
        # medición.
        type_unit_validations = measurement_type.validations.all()
        return type_unit_validations

    @swagger.operation(
        notes=(u'Crea una nueva instancia de validación de unidad de '
               'medición, asociada al tipo de medición especificado, y la '
               'retorna.').encode('utf-8'),
        responseClass='TypeUnitValidationFields',
        nickname='typeUnitValidationList_post',
        parameters=[
            {
                "name": "measurement_type_id",
                "description": u'Identificador único del tipo de medición.'.encode('utf-8'),
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
                "name": "measurement_unit_id",
                "description": u'Identificador único de la unidad de medición.'.encode('utf-8'),
                "required": True,
                "dataType": "int",
                "paramType": "body"
            },
        ],
        responseMessages=[
            code_201_created,
            code_404
        ]
    )
    @marshal_with(TypeUnitValidationFields.resource_fields, envelope='resource')
    def post(self, measurement_type_id):
        # Obtiene el tipo de medición.
        measurement_type = MeasurementType.query.get_or_404(measurement_type_id)

        # Obtiene los valores de los argumentos recibidos en la petición.
        args = parser_post.parse_args()
        min_value = args['min_value']
        max_value = args['max_value']
        measurement_unit_id = args['measurement_unit_id']

        # Obtiene la unidad de medición.
        measurement_unit = MeasurementUnit.query.get_or_404(measurement_unit_id)

        # Crea la nueva validación de unidad de medida.
        new_type_unit_validation = TypeUnitValidation(min_value,
                                                      max_value,
                                                      measurement_type.id,
                                                      measurement_unit.id)
        db.session.add(new_type_unit_validation)

        db.session.commit()
        return new_type_unit_validation, 201
