# -*- coding: utf-8 -*-

from flask import g
from flask_restful import Resource, marshal_with
from flask_restful_swagger import swagger

from app.mod_shared.models.auth import auth
from app.mod_profiles.common.fields.userStatisticsFields import UserStatisticsFields
from app.mod_profiles.common.persistence.statistics import get_encryption_percentage
from app.mod_profiles.common.swagger.responses.generic_responses import code_200_ok, code_401


class MyStatisticsView(Resource):
    @swagger.operation(
        notes=u'Retorna las estadísticas del usuario autenticado.'.encode('utf-8'),
        responseClass='UserStatisticsFields',
        nickname='myStatisticsView_get',
        responseMessages=[
            code_200_ok,
            code_401,
        ]
    )
    @auth.login_required
    @marshal_with(UserStatisticsFields.resource_fields, envelope='resource')
    def get(self):
        # Obtiene el perfil asociado al usuario autenticado.
        profile = g.user.profile

        # Crea la respuesta por defecto.
        response = {
            'encryption_percentage': get_encryption_percentage(profile),
        }

        return response, 200
