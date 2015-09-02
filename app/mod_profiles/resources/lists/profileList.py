# -*- coding: utf-8 -*-

from flask_restful import Resource, reqparse, marshal_with
from flask_restful_swagger import swagger
from app.mod_shared.models.db import db
from app.mod_profiles.models import Profile
from app.mod_profiles.resources.fields.profileFields import ProfileFields
from app.mod_profiles.validators.globalValidator import string_without_int,
positive_int

parser = reqparse.RequestParser()
parser.add_argument('last_name', type=string_without_int, required=True)
parser.add_argument('first_name', type=string_without_int, required=True)
parser.add_argument('gender_id', type=positive_int)
parser.add_argument('birthday')

class ProfileList(Resource):
    @swagger.operation(
        notes=u'Retorna todas las instancias existentes de perfil.'.encode('utf-8'),
        responseClass='ProfileFields',
        nickname='profileList_get',
        responseMessages=[
            {
              "code": 200,
              "message": "Solicitud resuelta exitosamente."
            }
          ]
        )
    @marshal_with(ProfileFields.resource_fields, envelope='resource')
    def get(self):
        profiles = Profile.query.all()
        return profiles

    @swagger.operation(
        notes=u'Crea una nueva instancia de perfil, y la retorna.'.encode('utf-8'),
        responseClass='ProfileFields',
        nickname='profileList_post',
        parameters=[
            {
              "name": "id",
              "description": u'Identificador único del perfil.'.encode('utf-8'),
              "required": True,
              "dataType": "int",
              "paramType": "path"
            },
            {
              "name": "last_name",
              "description": u'Apellido de la persona.'.encode('utf-8'),
              "required": True,
              "dataType": "string",
              "paramType": "body"
            },
            {
              "name": "first_name",
              "description": u'Nombre de la persona.'.encode('utf-8'),
              "required": True,
              "dataType": "string",
              "paramType": "body"
            },
            {
              "name": "birthday",
              "description": u'Fecha de nacimiento de la persona, en formato ISO 8601.'.encode('utf-8'),
              "required": False,
              "dataType": "datetime",
              "paramType": "body"
            },
            {
              "name": "gender_id",
              "description": u'Identificador único del género asociado.'.encode('utf-8'),
              "required": False,
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
    @marshal_with(ProfileFields.resource_fields, envelope='resource')
    def post(self):
        args = parser.parse_args()
        new_profile = Profile(args['last_name'],
                              args['first_name'],
                              args['birthday'],
                              args['gender_id'])
        db.session.add(new_profile)
        db.session.commit()
        return new_profile, 201
