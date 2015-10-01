# -*- coding: utf-8 -*-

from flask_restful import Resource, marshal_with
from flask_restful_swagger import swagger

from app.mod_profiles.common.persistence.profile import update
from app.mod_profiles.models import Profile
from app.mod_profiles.common.fields.profileFields import ProfileFields
from app.mod_profiles.common.parsers.profile import parser_put
from app.mod_profiles.common.swagger.responses.generic_responses import code_200_found, code_200_updated, code_404


class ProfileView(Resource):
    @swagger.operation(
        notes=u'Retorna una instancia específica de perfil.'.encode('utf-8'),
        responseClass='ProfileFields',
        nickname='profileView_get',
        parameters=[
            {
              "name": "id",
              "description": u'Identificador único del perfil.'.encode('utf-8'),
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
    @marshal_with(ProfileFields.resource_fields, envelope='resource')
    def get(self, id):
        profile = Profile.query.get_or_404(id)
        return profile

    @swagger.operation(
        notes=u'Actualiza una instancia específica de perfil, y la retorna.'.encode('utf-8'),
        responseClass='ProfileFields',
        nickname='profileView_put',
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
            code_200_updated,
            code_404
        ]
    )
    @marshal_with(ProfileFields.resource_fields, envelope='resource')
    def put(self, id):
        # Obtiene el perfil.
        profile = Profile.query.get_or_404(id)

        # Obtiene los valores de los argumentos recibidos en la petición.
        args = parser_put.parse_args()
        first_name = args['first_name']
        last_name = args['last_name']
        birthday = args['birthday']
        gender_id = args['gender_id']

        # Actualiza los atributos y relaciones del objeto, en base a los
        # argumentos recibidos.
        updated_profile = update(
            profile=profile,
            first_name=first_name,
            last_name=last_name,
            birthday=birthday,
            gender_id=gender_id
        )

        return updated_profile, 200
