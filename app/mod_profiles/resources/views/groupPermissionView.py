# -*- coding: utf-8 -*-

from flask import g
from flask_restful import Resource, marshal_with
from flask_restful_swagger import swagger

from app.mod_shared.models.auth import auth
from app.mod_shared.models.db import db
from app.mod_profiles.models import GroupPermission
from app.mod_profiles.common.fields.groupPermissionFields import GroupPermissionFields
from app.mod_profiles.common.swagger.responses.generic_responses import code_200_found, code_204_deleted, \
    code_401, code_403, code_404


class GroupPermissionView(Resource):
    @swagger.operation(
        notes=u'Retorna una instancia específica de permiso de grupo.'.encode('utf-8'),
        responseClass='GroupPermissionFields',
        nickname='groupPermissionView_get',
        parameters=[
            {
                "name": "group_permission_id",
                "description": u'Identificador único del permiso de grupo.'.encode('utf-8'),
                "required": True,
                "dataType": "int",
                "paramType": "path"
            },
        ],
        responseMessages=[
            code_200_found,
            code_404,
        ],
    )
    @marshal_with(GroupPermissionFields.resource_fields, envelope='resource')
    def get(self, group_permission_id):
        group_permission = GroupPermission.query.get_or_404(group_permission_id)
        return group_permission

    @swagger.operation(
        notes=u'Elimina una instancia específica de permiso de grupo.'.encode('utf-8'),
        nickname='groupPermissionView_delete',
        parameters=[
            {
                "name": "group_permission_id",
                "description": u'Identificador único del permiso de grupo.'.encode('utf-8'),
                "required": True,
                "dataType": "int",
                "paramType": "path"
            },
        ],
        responseMessages=[
            code_204_deleted,
            code_401,
            code_403,
            code_404,
        ],
    )
    @auth.login_required
    @marshal_with(GroupPermissionFields.resource_fields, envelope='resource')
    def delete(self, group_permission_id):
        # Obtiene el permiso de grupo.
        group_permission = GroupPermission.query.get_or_404(group_permission_id)

        # Verifica que el usuario autenticado sea el dueño del análisis
        # asociado al permiso especificado.
        if g.user.id != group_permission.analysis.profile.user.first().id:
            return '', 403

        # Elimina el permiso de grupo.
        db.session.delete(group_permission)
        db.session.commit()

        return '', 204
