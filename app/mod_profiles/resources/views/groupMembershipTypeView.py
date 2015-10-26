# -*- coding: utf-8 -*-

from flask_restful import Resource, marshal_with
from flask_restful_swagger import swagger

from app.mod_shared.models.db import db
from app.mod_profiles.models import GroupMembershipType
from app.mod_profiles.common.fields.groupMembershipTypeFields import GroupMembershipTypeFields
from app.mod_profiles.common.parsers.groupMembershipType import parser_put
from app.mod_profiles.common.swagger.responses.generic_responses import code_200_found, code_200_updated, code_404


class GroupMembershipTypeView(Resource):
    @swagger.operation(
        notes=u'Retorna una instancia específica de tipo de membresía de grupo.'.encode('utf-8'),
        responseClass='GroupMembershipTypeFields',
        nickname='groupMembershipTypeView_get',
        parameters=[
            {
                "name": "group_membership_type_id",
                "description": (u'Identificador único del tipo de membresía '
                                'de grupo.').encode('utf-8'),
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
    @marshal_with(GroupMembershipTypeFields.resource_fields, envelope='resource')
    def get(self, group_membership_type_id):
        group_membership_type = GroupMembershipType.query.get_or_404(group_membership_type_id)
        return group_membership_type

    @swagger.operation(
        notes=(u'Actualiza una instancia específica de tipo de membresía de '
               'grupo, y la retorna.').encode('utf-8'),
        responseClass='GroupMembershipTypeFields',
        nickname='groupMembershipTypeView_put',
        parameters=[
            {
                "name": "group_membership_type_id",
                "description": (u'Identificador único del tipo de membresía '
                                'de grupo.').encode('utf-8'),
                "required": True,
                "dataType": "int",
                "paramType": "path"
            },
            {
                "name": "name",
                "description": u'Nombre del tipo de membresía de grupo.'.encode('utf-8'),
                "required": True,
                "dataType": "string",
                "paramType": "body"
            },
            {
                "name": "description",
                "description": u'Descripción del tipo de membresía de grupo.'.encode('utf-8'),
                "required": False,
                "dataType": "string",
                "paramType": "body"
            },
        ],
        responseMessages=[
            code_200_updated,
            code_404
        ]
    )
    @marshal_with(GroupMembershipTypeFields.resource_fields, envelope='resource')
    def put(self, group_membership_type_id):
        # Obtiene el tipo de membresía de grupo.
        group_membership_type = GroupMembershipType.query.get_or_404(group_membership_type_id)

        # Obtiene los valores de los argumentos recibidos en la petición.
        args = parser_put.parse_args()
        name = args['name']
        description = args['description']

        # Actualiza los atributos y relaciones del objeto, en base a los
        # argumentos recibidos.

        # Actualiza el nombre, en caso de que haya sido modificado.
        if (name is not None and
                group_membership_type.name != name):
            group_membership_type.name = name
        # Actualiza la descripción, en caso de que haya sido modificada.
        if (description is not None and
                group_membership_type.description != description):
            group_membership_type.description = description

        db.session.commit()
        return group_membership_type, 200
