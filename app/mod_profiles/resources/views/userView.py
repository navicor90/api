# -*- coding: utf-8 -*-

from flask_restful import Resource, reqparse, marshal_with
from flask_restful_swagger import swagger
from app.mod_shared.models.db import db
from app.mod_profiles.models import User
from app.mod_profiles.resources.fields.userFields import UserFields

parser = reqparse.RequestParser()
parser.add_argument('username', type=str, required=True)
parser.add_argument('email', type=str, required=True)
parser.add_argument('password', type=str, required=True)
parser.add_argument('profile_id', type=int, required=True)

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
            {
              "code": 200,
              "message": "Objeto encontrado."
            },
            {
              "code": 404,
              "message": "Objeto inexistente."
            }
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
            {
              "code": 200,
              "message": "Objeto actualizado exitosamente."
            },
            {
              "code": 404,
              "message": "Objeto inexistente."
            }
          ]
        )
    @marshal_with(UserFields.resource_fields, envelope='resource')
    def put(self, id):
        user = User.query.get_or_404(id)
        args = parser.parse_args()

        # Actualiza los atributos y relaciones del objeto, en base a los
        # argumentos recibidos.

        # Actualiza el nombre de usuario, en caso de que haya sido modificado.
        if (args['username'] is not None and
              user.username != args['username']):
            user.username = args['username']
        # Actualiza la dirección de correo electrónico, en caso de que haya
        # sido modificado.
        if (args['email'] is not None and
              user.email != args['email']):
            user.email = args['email']
        # Actualiza la contraseña, en caso de que haya sido modificado.
        if (args['password'] is not None and
              not user.verify_password(args['password'])):
            user.hash_password(args['password'])
        # Actualiza el perfil asociado, en caso de que haya sido modificado.
        if (args['profile_id'] is not None and
              user.profile_id != args['profile_id']):
            user.profile_id = args['profile_id']

        db.session.commit()
        return user, 200