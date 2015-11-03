# -*- coding: utf-8 -*-

from flask import g
from flask_restful import Resource, marshal_with
from flask_restful_swagger import swagger

from app.mod_shared.models.auth import auth
from app.mod_profiles.common.fields.profileFields import ProfileFields
from app.mod_profiles.common.swagger.responses.generic_responses import code_200_found, code_401


class MySharedAnalysisProfileList(Resource):
    @swagger.operation(
        # TODO: Añadir parámetros de autenticación a la documentación Swagger.
        notes=(u'Retorna todos los perfiles de usuario, que son dueños de '
               'análisis sobre los cuales el usuario autenticado tiene '
               'permisos.').encode('utf-8'),
        responseClass='ProfileFields',
        nickname='mySharedAnalysisProfileList_get',
        responseMessages=[
            code_200_found,
            code_401
        ]
    )
    @auth.login_required
    @marshal_with(ProfileFields.resource_fields, envelope='resource')
    def get(self):
        # Obtiene los permisos asociados al usuario.
        permissions = g.user.permissions.all()

        # Por cada permiso, obtiene el dueño del análisis asociado al mismo.
        analysis_profiles = set()
        for permission in permissions:
            analysis_profiles.add(permission.analysis.profile)

        analysis_profiles = list(analysis_profiles)
        return analysis_profiles
