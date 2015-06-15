# -*- coding: utf-8 -*-

from flask_restful import Resource, reqparse, marshal_with
from flask_restful_swagger import swagger
from app.mod_shared.models import db
from app.mod_profiles.models import *
from .genderFields import GenderFields

parser = reqparse.RequestParser()
parser.add_argument('name', type=str, required=True)
parser.add_argument('description', type=str)

class GenderList(Resource):
    @swagger.operation(
        notes=u'Retorna todas las instancias existentes de género.'.encode('utf-8'),
        responseClass='GenderFields',
        nickname='genderList_get',
        responseMessages=[
            {
              "code": 200,
              "message": "Solicitud resuelta exitosamente."
            }
          ]
        )
    @marshal_with(GenderFields.resource_fields, envelope='resource')
    def get(self):
        genders = Gender.query.all()
        return genders

    @swagger.operation(
        notes=u'Crea una nueva instancia de género, y la retorna.'.encode('utf-8'),
        responseClass='GenderFields',
        nickname='genderList_post',
        parameters=[
            {
              "name": "name",
              "description": u'Nombre del género.'.encode('utf-8'),
              "required": True,
              "dataType": "string",
              "paramType": "body"
            },
            {
              "name": "description",
              "description": u'Descripción del género.'.encode('utf-8'),
              "required": False,
              "dataType": "string",
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
    @marshal_with(GenderFields.resource_fields, envelope='resource')
    def post(self):
        args = parser.parse_args()
        new_gender = Gender(args['name'],
                            args['description'])
        db.session.add(new_gender)
        db.session.commit()
        return new_gender, 201
