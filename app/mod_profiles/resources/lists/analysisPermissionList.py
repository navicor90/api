# -*- coding: utf-8 -*-

from flask import g
from flask_restful import Resource, marshal_with
from flask_restful_swagger import swagger

from app.mod_shared.models.auth import auth
from app.mod_shared.models.db import db
from app.mod_profiles.models import Analysis, Permission
from app.mod_profiles.common.fields.permissionFields import PermissionFields
from app.mod_profiles.common.parsers.permission import parser_post
from app.mod_profiles.common.swagger.responses.generic_responses import code_200_ok, code_201_created, code_401, \
    code_403, code_404


class AnalysisPermissionList(Resource):
    @swagger.operation(
        notes=(u'Retorna todas las instancias existentes de permisos, del '
               'análisis especificado.').encode('utf-8'),
        responseClass='PermissionFields',
        nickname='analysisPermissionList_get',
        responseMessages=[
            code_200_ok,
            code_404
        ]
    )
    @marshal_with(PermissionFields.resource_fields, envelope='resource')
    def get(self, analysis_id):
        # Obtiene el análisis.
        analysis = Analysis.query.get_or_404(analysis_id)

        # Obtiene los permisos del análisis.
        analysis_permissions = analysis.permissions
        return analysis_permissions

    @swagger.operation(
        notes=(u'Crea una nueva instancia de permiso asociada al análisis, y '
               'la retorna.').encode('utf-8'),
        responseClass='PermissionFields',
        nickname='analysisPermissionList_post',
        parameters=[
            {
                "name": "analysis_id",
                "description": u'Identificador único del análisis asociado.'.encode('utf-8'),
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
            {
                "name": "user_id",
                "description": u'Identificador único del usuario asociado.'.encode('utf-8'),
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
    @marshal_with(PermissionFields.resource_fields, envelope='resource')
    def post(self, analysis_id):
        # Obtiene el análisis.
        analysis = Analysis.query.get_or_404(analysis_id)

        # Verifica que el usuario autenticado sea el dueño del análisis
        # especificado.
        if g.user.id != analysis.profile.user.first().id:
            return '', 403

        # Obtiene los valores de los argumentos recibidos en la petición.
        args = parser_post.parse_args()
        permission_type_id = args['permission_type_id']
        user_id = args['user_id']

        # Obtiene los permisos del análisis.
        analysis_permissions = analysis.permissions

        # Verifica que el análisis no tenga un permiso existente asociado al
        # mismo usuario especificado en la solicitud.
        for permission in analysis_permissions:
            # En caso de que exista un permiso con estas características, se
            # elimina.
            if user_id == permission.user.id:
                db.session.delete(permission)

        # Crea un nuevo permiso, con los datos provistos.
        new_permission = Permission(analysis_id,
                                    permission_type_id,
                                    user_id)

        db.session.add(new_permission)
        db.session.commit()
        return new_permission, 201
