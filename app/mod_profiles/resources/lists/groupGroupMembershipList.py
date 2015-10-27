# -*- coding: utf-8 -*-

from datetime import datetime
from flask import g
from flask_restful import Resource, marshal_with
from flask_restful_swagger import swagger

from app.mod_shared.models.auth import auth
from app.mod_shared.models.db import db
from app.mod_profiles.models import Group, GroupMembership, GroupMembershipType, PermissionType, User
from app.mod_profiles.common.fields.groupMembershipFields import GroupMembershipFields
from app.mod_profiles.common.parsers.groupMembership import parser_post_auth
from app.mod_profiles.common.persistence import group as group_persistence
from app.mod_profiles.common.swagger.responses.generic_responses import code_200_ok, code_201_created, code_401, \
    code_403, code_404


class GroupGroupMembershipList(Resource):
    # Crea una copia de los campos del modelo 'GroupMembership'.
    resource_fields = GroupMembershipFields.resource_fields.copy()
    # Quita el grupo asociado de los campos del recurso.
    del resource_fields['group']

    @swagger.operation(
        notes=(u'Retorna todas las instancias existentes de membresías de '
               'grupo, asociadas a un grupo específico.').encode('utf-8'),
        responseClass='GroupMembershipFields',
        nickname='groupGroupMembershipList_get',
        parameters=[
            {
                "name": "group_id",
                "description": u'Identificador único del grupo.'.encode('utf-8'),
                "required": True,
                "dataType": "int",
                "paramType": "path"
            },
        ],
        responseMessages=[
            code_200_ok,
            code_401,
            code_403,
            code_404
        ]
    )
    @auth.login_required
    @marshal_with(resource_fields, envelope='resource')
    def get(self, group_id):
        # Obtiene el grupo.
        group = Group.query.get_or_404(group_id)

        # Verifica que el usuario autenticado sea miembro del grupo
        # especificado.
        if not group_persistence.is_group_member(group, g.user):
            return '', 403

        # Obtiene todas las membresías asociadas al grupo.
        group_memberships = group.memberships.all()
        return group_memberships

    @swagger.operation(
        # TODO: Añadir parámetros de autenticación a la documentación Swagger.
        notes=(u'Crea una nueva instancia de membresía de grupo, asociada al '
               'perfil del usuario indicado y al grupo especificado, y la '
               'retorna.').encode('utf-8'),
        responseClass='GroupMembershipList',
        nickname='groupGroupMembershipList_post',
        parameters=[
            {
                "name": "group_id",
                "description": u'Identificador único del grupo.'.encode('utf-8'),
                "required": True,
                "dataType": "int",
                "paramType": "path"
            },
            {
                "name": "is_admin",
                "description": (u'Variable que indica si la membresía es de '
                                'administrador del grupo.').encode('utf-8'),
                "required": True,
                "dataType": "boolean",
                "paramType": "body"
            },
            {
                "name": "group_membership_type_id",
                "description": (u'Identificador único del tipo de membresía '
                                'de grupo asociado.').encode('utf-8'),
                "required": True,
                "dataType": "int",
                "paramType": "body"
            },
            {
                "name": "permission_type_id",
                "description": (u'Identificador único del tipo de permiso '
                                'asociado.').encode('utf-8'),
                "required": True,
                "dataType": "int",
                "paramType": "body"
            },
            {
                "name": "user_id",
                "description": (u'Identificador único del usuario dueño del '
                                'perfil asociado.').encode('utf-8'),
                "required": True,
                "dataType": "int",
                "paramType": "body"
            },
        ],
        responseMessages=[
            code_201_created,
            code_401,
            code_403
        ]
    )
    @auth.login_required
    @marshal_with(GroupMembershipFields.resource_fields, envelope='resource')
    def post(self, group_id):
        # Obtiene el grupo.
        group = Group.query.get_or_404(group_id)

        # Verifica que el usuario autenticado sea administrador del grupo
        # especificado.
        if not group_persistence.is_group_admin(group, g.user):
            return '', 403

        # Obtiene los valores de los argumentos recibidos en la petición.
        args = parser_post_auth.parse_args()
        is_admin = args['is_admin']
        group_membership_type_id = args['group_membership_type_id']
        permission_type_id = args['permission_type_id']
        user_id = args['user_id']

        # Obtiene el tipo de membresía de grupo.
        group_membership_type = GroupMembershipType.query.get_or_404(group_membership_type_id)

        # Obtiene el tipo de permiso.
        permission_type = PermissionType.query.get_or_404(permission_type_id)

        # Obtiene el usuario especificado.
        user = User.query.get_or_404(user_id)

        # Obtiene las membresías existentes del grupo.
        group_memberships = group.memberships.all()

        # Verifica que el grupo no tenga una membresía existente asociada al
        # mismo perfil especificado en la solicitud.
        for membership in group_memberships:
            # En caso de que exista una membresía con estas características, se
            # elimina.
            if user_id == membership.profile.user.first().id:
                db.session.delete(membership)

        # Crea la nueva membresía de grupo.
        new_group_membership = GroupMembership(is_admin,
                                               group.id,
                                               group_membership_type.id,
                                               permission_type.id,
                                               g.user.profile.id
                                               )
        db.session.add(new_group_membership)
        db.session.commit()
        return new_group_membership, 201
