# -*- coding: utf-8 -*-

from flask_restful import Resource, marshal_with
from flask_restful_swagger import swagger

from app.mod_shared.models.db import db
from app.mod_profiles.models import Gender
from app.mod_profiles.common.fields.genderFields import GenderFields
from app.mod_profiles.common.parsers.gender import parser_post
from app.mod_profiles.common.swagger.responses.generic_responses import code_200_ok, code_201_created


class GenderList(Resource):
    @swagger.operation(
        notes=u'Retorna todas las instancias existentes de género.'.encode('utf-8'),
        responseClass='GenderFields',
        nickname='genderList_get',
        responseMessages=[
            code_200_ok
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
            code_201_created
        ]
    )
    @marshal_with(GenderFields.resource_fields, envelope='resource')
    def post(self):
        args = parser_post.parse_args()
        new_gender = Gender(args['name'],
                            args['description'])
        db.session.add(new_gender)
        db.session.commit()
        return new_gender, 201
