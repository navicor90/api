# -*- coding: utf-8 -*-

from flask import g
from flask_restful import Resource, marshal_with
from flask_restful_swagger import swagger

from app.mod_shared.models.auth import auth
from app.mod_shared.models.db import db
from app.mod_profiles.models import Permission
from app.mod_profiles.common.fields.permissionFields import PermissionFields
from app.mod_profiles.common.parsers.permission import parser_put
from app.mod_profiles.common.swagger.responses.generic_responses import code_200_found, code_200_updated, \
    code_204_deleted, code_401, code_403, code_404


class PermissionView(Resource):
    @swagger.operation(
        notes=u'Retorna una instancia específica de permiso.'.encode('utf-8'),
        responseClass='PermissionFields',
        nickname='permissionView_get',
        parameters=[
            {
                "name": "permission_id",
                "description": u'Identificador único del permiso.'.encode('utf-8'),
                "required": True,
                "dataType": "int",
                "paramType": "path"
            },
        ],
        responseMessages=[
            code_200_found,
            code_404
        ]
    )
    @marshal_with(PermissionFields.resource_fields, envelope='resource')
    def get(self, permission_id):
        permission = Permission.query.get_or_404(permission_id)
        return permission

    @swagger.operation(
        notes=(u'Actualiza una instancia específica de permiso, y la retorna. '
               'Sólo permite modificar el tipo de permiso, no pudiendo '
               'cambiarse el usuario ni el análisis asociado. Para esto, debe '
               'crearse un nuevo permiso.').encode('utf-8'),
        responseClass='PermissionFields',
        nickname='permissionView_put',
        parameters=[
            {
                "name": "permission_id",
                "description": u'Identificador único del permiso.'.encode('utf-8'),
                "required": True,
                "dataType": "int",
                "paramType": "path"
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
    @marshal_with(PermissionFields.resource_fields, envelope='resource')
    def put(self, permission_id):
        # Obtiene el permiso.
        permission = Permission.query.get_or_404(permission_id)

        # Verifica que el usuario autenticado sea el dueño del análisis
        # asociado al permiso especificado.
        if g.user.id != permission.analysis.profile.user.first().id:
            return '', 403

        # Obtiene los valores de los argumentos recibidos en la petición.
        args = parser_put.parse_args()
        permission_type_id = args['permission_type_id']

        # Actualiza los atributos y relaciones del objeto, en base a los
        # argumentos recibidos.

        # Actualiza el tipo de permiso asociado, en caso de que haya sido
        # modificado.
        if (permission_type_id is not None and
                permission.permission_type_id != permission_type_id):
            permission.permission_type_id_id = permission_type_id

        db.session.commit()
        return permission, 200

    @swagger.operation(
        notes=u'Elimina una instancia específica de permiso.'.encode('utf-8'),
        nickname='permissionView_delete',
        parameters=[
            {
                "name": "permission_id",
                "description": u'Identificador único del permiso.'.encode('utf-8'),
                "required": True,
                "dataType": "int",
                "paramType": "path"
            },
        ],
        responseMessages=[
            code_204_deleted,
            code_401,
            code_403,
            code_404
        ]
    )
    @marshal_with(PermissionFields.resource_fields, envelope='resource')
    def delete(self, permission_id):
        # Obtiene el permiso.
        permission = Permission.query.get_or_404(permission_id)

        # Verifica que el usuario autenticado sea el dueño del análisis
        # asociado al permiso especificado.
        if g.user.id != permission.analysis.profile.user.first().id:
            return '', 403

        # Elimina el permiso.
        db.session.delete(permission)
        db.session.commit()

        return '', 204
