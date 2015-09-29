# -*- coding: utf-8 -*-

from flask_restful import Resource, marshal_with
from flask_restful_swagger import swagger

from app.mod_profiles.common.persistence.user import update
from app.mod_profiles.models import User
from app.mod_profiles.common.fields.userFields import UserFields
from app.mod_profiles.common.parsers.user import parser_put
from app.mod_profiles.common.swagger.responses.generic_responses import code_200_found, code_200_updated, code_404


class UserView(Resource):
    @swagger.operation(
        notes=u'Retorna una instancia específica de usuario.'.encode('utf-8'),
        responseClass='UserFields',
        nickname='userView_get',
        parameters=[
            {
              "name": "id",
              "description": u'Identificador único del usuario.'.encode('utf-8'),
              "required": True,
              "dataType": "int",
              "paramType": "path"
            }
          ],
        responseMessages=[
            code_200_found,
            code_404
        ]
    )
    @marshal_with(UserFields.resource_fields, envelope='resource')
    def get(self, id):
        user = User.query.get_or_404(id)
        return user

    @swagger.operation(
        notes=u'Actualiza una instancia específica de usuario, y la retorna.'.encode('utf-8'),
        responseClass='UserFields',
        nickname='userView_put',
        parameters=[
            {
              "name": "id",
              "description": u'Identificador único del usuario.'.encode('utf-8'),
              "required": True,
              "dataType": "int",
              "paramType": "path"
            },
            {
              "name": "username",
              "description": u'Nombre de usuario.'.encode('utf-8'),
              "required": True,
              "dataType": "string",
              "paramType": "body"
            },
            {
              "name": "email",
              "description": u'Dirección de correo electrónico del usuario.'.encode('utf-8'),
              "required": True,
              "dataType": "string",
              "paramType": "body"
            },
            {
              "name": "password",
              "description": u'Contraseña del usuario.'.encode('utf-8'),
              "required": True,
              "dataType": "string",
              "paramType": "body"
            },
            {
              "name": "profile_id",
              "description": u'Identificador único del perfil asociado.'.encode('utf-8'),
              "required": True,
              "dataType": "int",
              "paramType": "body"
            }
          ],
        responseMessages=[
            code_200_updated,
            code_404
        ]
    )
    @marshal_with(UserFields.resource_fields, envelope='resource')
    def put(self, id):
        # Obtiene el usuario.
        user = User.query.get_or_404(id)

        # Obtiene los valores de los argumentos recibidos en la petición.
        args = parser_put.parse_args()
        username = args['username']
        email = args['email']
        password = args['password']
        profile_id = args['profile_id']

        # Actualiza los atributos y relaciones del objeto, en base a los
        # argumentos recibidos.
        updated_user = update(
            user=user,
            username=username,
            email=email,
            password=password,
            profile_id=profile_id
        )

        return updated_user, 200
