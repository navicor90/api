# -*- coding: utf-8 -*-

from flask import g
from flask_restful import Resource, marshal_with
from flask_restful_swagger import swagger

from app.mod_shared.models.auth import auth
from app.mod_profiles.common.fields.analysisFields import AnalysisFields
from app.mod_profiles.common.parsers.mySharedAnalyses import parser_get
from app.mod_profiles.common.swagger.responses.generic_responses import code_200_found, code_401


class MySharedAnalysesList(Resource):
    @swagger.operation(
        # TODO: Añadir parámetros de autenticación a la documentación Swagger.
        notes=(u'Retorna todas las instancias existentes de análisis, sobre '
               'las cuales el usuario autenticado tiene permisos.').encode('utf-8'),
        responseClass='AnalysisFields',
        nickname='mySharedAnalysesList_get',
        parameters=[
            {
                "name": "profile",
                "description": (u'Identificador único del perfil de usuario. '
                                'Permite filtrar los análisis, para sólo '
                                'obtener los asociados al perfil especificado.').encode('utf-8'),
                "required": False,
                "dataType": "int",
                "paramType": "query"
            },
        ],
        responseMessages=[
            code_200_found,
            code_401
        ]
    )
    @auth.login_required
    @marshal_with(AnalysisFields.resource_fields, envelope='resource')
    def get(self):
        # Obtiene los permisos asociados al usuario.
        permissions = g.user.permissions.all()

        # Obtiene los valores de los argumentos recibidos en la petición.
        args = parser_get.parse_args()
        profile_id = args['profile']

        # Por cada permiso, obtiene el análisis asociado al mismo.
        analyses = []
        for permission in permissions:
            # Verifica que no se haya especificado un perfil, o que el perfil
            # especificado coincida con el dueño del análisis.
            if (profile_id is None or
                    permission.analysis.profile.id == profile_id):
                analyses.append(permission.analysis)

        return analyses
