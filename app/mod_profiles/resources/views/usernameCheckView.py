# -*- coding: utf-8 -*-

from flask_restful import Resource
from flask_restful_swagger import swagger

from app.mod_profiles.models import User
from app.mod_profiles.common.parsers.usernameCheck import parser_get
from app.mod_profiles.common.swagger.responses.generic_responses import code_200_found, code_204_empty


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
            code_200_found,
            code_204_empty
        ]
    )
    def get(self):
        # Obtiene los valores de los argumentos recibidos en la petición.
        args = parser_get.parse_args()
        username = args['username']

        # Busca si existe un usuario con el nombre de usuario especificado.
        user = User.query.filter_by(username=username).first()

        # Si el nombre de usuario está disponible, ya que no hay un usuario que
        # haga uso del mismo, se retorna un código 204.
        if not user:
            return '', 204
        # Si el nombre de usuario se encuentra en uso actualmente, se retorna
        # un código 200.
        return '', 200
