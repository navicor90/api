# -*- coding: utf-8 -*-

from flask import g
from flask_restful import Resource, marshal_with
from flask_restful_swagger import swagger

from app.mod_shared.models.auth import auth
from app.mod_profiles.common.fields.groupFields import GroupFields
from app.mod_profiles.common.swagger.responses.generic_responses import code_200_found, code_401, code_404


class MyGroupList(Resource):
    @swagger.operation(
        # TODO: Añadir parámetros de autenticación a la documentación Swagger.
        notes=(u'Retorna todas las instancias existentes de grupos, '
               'en las que el usuario autenticado tiene membresía.').encode('utf-8'),
        responseClass='GroupFields',
        nickname='myGroupList_get',
        responseMessages=[
            code_200_found,
            code_401,
            code_404
        ]
    )
    @auth.login_required
    @marshal_with(GroupFields.resource_fields, envelope='resource')
    def get(self):
        # Obtiene el perfil.
        profile = g.user.profile

        profile_groups = []

        # Obtiene todas las membresías de grupo asociadas al perfil.
        profile_memberships = profile.memberships.all()

        # Obtiene el grupo asociado a cada membresía de grupo.
        for membership in profile_memberships:
            profile_groups.append(membership.group)

        return profile_groups
