# -*- coding: utf-8 -*-

from flask import g
from flask_restful import Resource, marshal_with
from flask_restful_swagger import swagger

from app.mod_shared.models.auth import auth
from app.mod_shared.models.db import db
from app.mod_profiles.common.fields.groupFields import GroupFields
from app.mod_profiles.common.parsers.gender import parser_post
from app.mod_profiles.common.swagger.responses.generic_responses import code_201_created, code_404
from app.mod_profiles.models import Group, GroupMembership, GroupMembershipType, PermissionType


class GroupList(Resource):
    @swagger.operation(
        notes=(u'Crea una nueva instancia de grupo, y una membresía de grupo '
               'asociada al perfil del usuario autenticado. Retorna la '
               'instancia de grupo.').encode('utf-8'),
        responseClass='GroupFields',
        nickname='groupList_post',
        parameters=[
            {
                "name": "name",
                "description": u'Nombre del grupo.'.encode('utf-8'),
                "required": True,
                "dataType": "string",
                "paramType": "body"
            },
            {
                "name": "description",
                "description": u'Descripción del grupo.'.encode('utf-8'),
                "required": False,
                "dataType": "string",
                "paramType": "body"
            },
            {
                "name": "group_membership_type_id",
                "description": (u'Identificador único del tipo de membresía '
                                'asociada a la nueva membresía del perfil '
                                'del usuario autenticado.').encode('utf-8'),
                "required": True,
                "dataType": "int",
                "paramType": "body"
            },
            {
                "name": "permission_type_id",
                "description": (u'Identificador único del tipo de permiso '
                                'asociado a la nueva membresía del perfil '
                                'del usuario autenticado.').encode('utf-8'),
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
    @auth.login_required
    @marshal_with(GroupFields.resource_fields, envelope='resource')
    def post(self):
        # Obtiene los valores de los argumentos recibidos en la petición.
        args = parser_post.parse_args()
        name = args['name']
        description = args['description']
        group_membership_type_id = args['group_membership_type_id']
        permission_type_id = args['permission_type_id']

        # Obtiene el tipo de membresía especificado.
        group_membership_type = GroupMembershipType.query.get_or_404(group_membership_type_id)

        # Obtiene el tipo de permiso especificado.
        permission_type = PermissionType.query.get_or_404(permission_type_id)

        # Obtiene el perfil asociado al usuario autenticado.
        profile = g.user.profile

        # Crea el nuevo grupo.
        new_group = Group(name,
                          description)
        db.session.add(new_group)

        # Crea la membresía asociada al nuevo grupo y al perfil del usuario
        # autenticado.
        new_group_membership = GroupMembership(True,
                                               new_group.id,
                                               group_membership_type.id,
                                               permission_type.id,
                                               profile.id)
        db.session.add(new_group_membership)

        db.session.commit()
        return new_group, 201
