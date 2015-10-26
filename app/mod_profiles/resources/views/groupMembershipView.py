# -*- coding: utf-8 -*-

from flask import g
from flask_restful import Resource, marshal_with
from flask_restful_swagger import swagger

from app.mod_shared.models.auth import auth
from app.mod_shared.models.db import db
from app.mod_profiles.models import GroupMembership, GroupMembershipType, PermissionType
from app.mod_profiles.common.fields.groupMembershipFields import GroupMembershipFields
from app.mod_profiles.common.parsers.groupMembership import parser_put
from app.mod_profiles.common.persistence import group as group_persistence
from app.mod_profiles.common.swagger.responses.generic_responses import code_200_found, code_200_updated, \
    code_204_deleted, code_401, code_403, code_404


class GroupMembershipView(Resource):
    @swagger.operation(
        notes=u'Retorna una instancia específica de membresía de grupo.'.encode('utf-8'),
        responseClass='MeasurementFields',
        nickname='measurementView_get',
        parameters=[
            {
                "name": "group_membership_id",
                "description": u'Identificador único de la membresía de grupo.'.encode('utf-8'),
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
    @marshal_with(GroupMembershipFields.resource_fields, envelope='resource')
    def get(self, group_membership_id):
        group_membership = GroupMembership.query.get_or_404(group_membership_id)
        return group_membership

    @swagger.operation(
        notes=(u'Actualiza una instancia específica de membresía de grupo, y '
               'la retorna.').encode('utf-8'),
        responseClass='GroupMembershipFields',
        nickname='groupMembershipView_put',
        parameters=[
            {
                "name": "group_membership_id",
                "description": u'Identificador único de la membresía de grupo.'.encode('utf-8'),
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
          ],
        responseMessages=[
            code_200_updated,
            code_401,
            code_403,
            code_404
        ]
    )
    @auth.login_required
    @marshal_with(GroupMembershipFields.resource_fields, envelope='resource')
    def put(self, group_membership_id):
        # Obtiene la membresía de grupo.
        group_membership = GroupMembership.query.get_or_404(group_membership_id)

        # Obtiene los valores de los argumentos recibidos en la petición.
        args = parser_put.parse_args()
        is_admin = args['is_admin']
        group_membership_type_id = args['group_membership_type_id']
        permission_type_id = args['permission_type_id']

        # Obtiene el tipo de membresía de grupo.
        group_membership_type = GroupMembershipType.query.get_or_404(group_membership_type_id)

        # Obtiene el tipo de permiso.
        permission_type = PermissionType.query.get_or_404(permission_type_id)

        # Verifica que el usuario autenticado sea administrador del grupo.
        if not group_persistence.is_group_admin(group_membership.group, g.user):
            return '', 403

        # Actualiza los atributos y relaciones del objeto, en base a los
        # argumentos recibidos.

        # Actualiza la indicación de administrador, en caso de que haya sido
        # modificada.
        if (is_admin is not None and
                group_membership.is_admin != is_admin):
            group_membership.is_admin = is_admin
        # Actualiza el tipo de membresía de grupo asociado, en caso de que haya
        # sido modificado.
        if (group_membership_type is not None and
                group_membership.group_membership_type != group_membership_type):
            group_membership.group_membership_type = group_membership_type
        # Actualiza el tipo de permiso asociado, en caso de que haya sido
        # modificado.
        if (permission_type is not None and
                group_membership.permission_type != permission_type):
            group_membership.permission_type = permission_type

        db.session.commit()
        return group_membership, 200

    @swagger.operation(
        notes=u'Elimina una instancia específica de membresía de grupo.'.encode('utf-8'),
        nickname='groupMembershipView_delete',
        parameters=[
            {
                "name": "group_membership_id",
                "description": u'Identificador único de la membresía de grupo.'.encode('utf-8'),
                "required": True,
                "dataType": "int",
                "paramType": "path"
            }
        ],
        responseMessages=[
            code_204_deleted,
            code_401,
            code_403,
            code_404
        ]
    )
    @auth.login_required
    @marshal_with(GroupMembershipFields.resource_fields, envelope='resource')
    def delete(self, group_membership_id):
        # Obtiene la membresía de grupo.
        group_membership = GroupMembership.query.get_or_404(group_membership_id)

        # Verifica que el usuario autenticado sea el dueño de la membresía, o
        # que sea administrador del grupo.
        if not (g.user.profile.id == group_membership.profile.id or
                group_persistence.is_group_admin(group_membership.group, g.user)):
            return '', 403

        # Elimina la membresía de grupo.
        db.session.delete(group_membership)
        db.session.commit()

        return '', 204
