# -*- coding: utf-8 -*-

from flask_restful import Resource, marshal_with
from flask_restful_swagger import swagger

from app.mod_profiles.models import User
from app.mod_profiles.common.fields.usernameCheckFields import UsernameCheckFields
from app.mod_profiles.common.parsers.usernameCheck import parser_get
from app.mod_profiles.common.swagger.responses.generic_responses import code_200_ok


class UsernameCheckView(Resource):
    @swagger.operation(
        notes=u'Verifica la disponibilidad de un nombre de usuario.'.encode('utf-8'),
        nickname='usernameCheckView_get',
        parameters=[
            {
              "name": "username",
              "description": u'Nombre de usuario a verificar.'.encode('utf-8'),
              "required": True,
              "dataType": "string",
              "paramType": "query"
            }
          ],
        responseMessages=[
            code_200_ok
        ]
    )
    @marshal_with(UsernameCheckFields.resource_fields, envelope='resource')
    def get(self):
        # Crea la respuesta por defecto.
        response = {'available_username': False}

        # Obtiene los valores de los argumentos recibidos en la petición.
        args = parser_get.parse_args()
        username = args['username']

        # Busca si existe un usuario con el nombre de usuario especificado.
        user = User.query.filter_by(username=username).first()

        # Verifica si el nombre de usuario está disponible, al no haber un
        # usuario que haga uso del mismo.
        if user is None:
            response['available_username'] = True

        return response, 200
