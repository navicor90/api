# -*- coding: utf-8 -*-

from flask import g
from flask_restful import Resource, marshal_with
from flask_restful_swagger import swagger

from app.mod_shared.models.auth import auth
from app.mod_shared.models.db import db
from app.mod_profiles.models import Analysis, Group, GroupPermission, NotificationNewSharedAnalysis
from app.mod_profiles.common.fields.groupPermissionFields import GroupPermissionFields
from app.mod_profiles.common.parsers.groupPermission import parser_post
from app.mod_profiles.common.persistence import group as group_persistence
from app.mod_profiles.common.swagger.responses.generic_responses import code_200_ok, code_201_created, code_401, \
    code_403, code_404


class AnalysisGroupPermissionList(Resource):
    @swagger.operation(
        notes=(u'Retorna todas las instancias existentes de permisos de '
               'grupo, del análisis especificado.').encode('utf-8'),
        responseClass='GroupPermissionFields',
        nickname='analysisGroupPermissionList_get',
        parameters=[
            {
                "name": "analysis_id",
                "description": u'Identificador único del análisis asociado.'.encode('utf-8'),
                "required": True,
                "dataType": "int",
                "paramType": "path"
            },
        ],
        responseMessages=[
            code_200_ok,
            code_404,
        ]
    )
    @marshal_with(GroupPermissionFields.resource_fields, envelope='resource')
    def get(self, analysis_id):
        # Obtiene el análisis.
        analysis = Analysis.query.get_or_404(analysis_id)

        # Obtiene los permisos de grupo del análisis.
        analysis_group_permissions = analysis.group_permissions.all()
        return analysis_group_permissions

    @swagger.operation(
        notes=(u'Crea una nueva instancia de permiso de grupo asociada al '
               'análisis, y la retorna.').encode('utf-8'),
        responseClass='GroupPermissionFields',
        nickname='analysisGroupPermissionList_post',
        parameters=[
            {
                "name": "analysis_id",
                "description": u'Identificador único del análisis asociado.'.encode('utf-8'),
                "required": True,
                "dataType": "int",
                "paramType": "path"
            },
            {
                "name": "group_id",
                "description": u'Identificador único del grupo asociado.'.encode('utf-8'),
                "required": True,
                "dataType": "int",
                "paramType": "body"
            },
        ],
        responseMessages=[
            code_201_created,
            code_401,
            code_403,
        ]
    )
    @auth.login_required
    @marshal_with(GroupPermissionFields.resource_fields, envelope='resource')
    def post(self, analysis_id):
        # Obtiene el análisis.
        analysis = Analysis.query.get_or_404(analysis_id)

        # Verifica que el usuario autenticado sea el dueño del análisis
        # especificado.
        if g.user.id != analysis.profile.user.first().id:
            return '', 403

        # Obtiene los valores de los argumentos recibidos en la petición.
        args = parser_post.parse_args()
        group_id = args['group_id']

        # Obtiene el grupo.
        group = Group.query.get_or_404(group_id)

        # Verifica que el usuario autenticado sea miembro del grupo
        # especificado.
        if not group_persistence.is_group_member(group, g.user):
            return '', 403

        # Obtiene los permisos de grupo del análisis.
        analysis_group_permissions = analysis.group_permissions.all()

        # Verifica que el análisis no tenga un permiso existente asociado al
        # mismo usuario especificado en la solicitud.
        for permission in analysis_group_permissions:
            # En caso de que exista un permiso con estas características, se
            # elimina.
            if group_id == permission.group.id:
                db.session.delete(permission)

        # Crea un nuevo permiso, con los datos provistos.
        new_group_permission = GroupPermission(analysis_id,
                                               group_id,
                                               )
        db.session.add(new_group_permission)
        db.session.flush()

        # Crea la notificación dirigida al resto de los integrantes del grupo.
        for membership in group.memberships.all():
            # Verifica que la membresía no pertenezca al usuario que realiza la
            # compartición.
            if g.user.profile.id != membership.profile.id:
                notification = NotificationNewSharedAnalysis(membership.profile.id,
                                                             g.user.profile.id,
                                                             new_group_permission.id,
                                                             )
                db.session.add(notification)

        db.session.commit()
        return new_group_permission, 201
