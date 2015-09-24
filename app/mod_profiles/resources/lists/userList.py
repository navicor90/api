# -*- coding: utf-8 -*-

from flask_restful import Resource, marshal_with
from flask_restful_swagger import swagger
from app.mod_shared.models.db import db
from app.mod_profiles.models import User
from app.mod_profiles.common.fields.userFields import UserFields
from app.mod_profiles.common.parsers.user import parser_post


class UserList(Resource):
    @swagger.operation(
        notes=u'Retorna todas las instancias existentes de usuario.'.encode('utf-8'),
        responseClass='UserFields',
        nickname='userList_get',
        responseMessages=[
            {
              "code": 200,
              "message": "Solicitud resuelta exitosamente."
            }
          ]
        )
    @marshal_with(UserFields.resource_fields, envelope='resource')
    def get(self):
        users = User.query.all()
        return users

    @swagger.operation(
        notes=u'Crea una nueva instancia de usuario, y la retorna.'.encode('utf-8'),
        responseClass='UserFields',
        nickname='userList_post',
        parameters=[
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
              "code": 201,
              "message": "Objeto creado exitosamente."
            }
          ]
        )
    @marshal_with(UserFields.resource_fields, envelope='resource')
    def post(self):
        args = parser_post.parse_args()
        username = args['username']
        if User.query.filter_by(username=username).first() is not None:
            # Usuario existente.
            return 400
        new_user = User(args['username'],
                            args['email'],
                            args['password'],
                            args['profile_id'])
        db.session.add(new_user)
        db.session.commit()
        return new_user, 201
