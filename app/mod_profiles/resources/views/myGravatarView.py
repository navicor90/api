# -*- coding: utf-8 -*-

from hashlib import md5
from urllib import urlencode
from flask import g
from flask_restful import Resource, marshal_with
from flask_restful_swagger import swagger

from app.mod_shared.models.auth import auth
from app.mod_profiles.common.fields.userGravatarFields import UserGravatarFields
from app.mod_profiles.common.parsers.userGravatar import parser_get
from app.mod_profiles.common.persistence.gravatar import get_gravatar_url
from app.mod_profiles.common.swagger.responses.generic_responses import code_200_found, code_404


class MyGravatarView(Resource):
    @swagger.operation(
        notes=(u'Retorna la dirección URL de la imagen Gravatar del usuario '
               'autenticado.').encode('utf-8'),
        responseClass='UserGravatarFields',
        nickname='myGravatarView_get',
        parameters=[
            {
                "name": "default",
                "description": (u'Imagen por defecto, en caso de no existir '
                                'un gravatar asociado a la dirección de '
                                'correo electrónico del usuario. Se permiten '
                                'direcciones web, o los valores soportados '
                                'por Gravatar. Por defecto, es "identicon" '
                                '(patrón geométrico basado en el correo '
                                'electrónico).').encode('utf-8'),
                "required": False,
                "dataType": "string",
                "paramType": "query"
            },
            {
                "name": "size",
                "description": (u'Tamaño en píxeles de la imagen solicitada. '
                                'Debido a que son imágenes cuadradas, sólo se '
                                'requiere un número, entre 1 y 2048. Por '
                                'defecto, la imagen es de 80px.').encode('utf-8'),
                "required": False,
                "dataType": "int",
                "paramType": "query"
            },
        ],
        responseMessages=[
            code_200_found,
            code_404
        ]
    )
    @auth.login_required
    @marshal_with(UserGravatarFields.resource_fields, envelope='resource')
    def get(self):
        # Obtiene los valores de los argumentos recibidos en la petición.
        args = parser_get.parse_args()
        default = args['default'] or 'identicon'
        size = args['size'] or 80

        # Obtiene la dirección URL del Gravatar del usuario.
        gravatar_url = get_gravatar_url(g.user, default, size)

        # Crea la respuesta a retornar.
        response = {
            'gravatar_url': gravatar_url,
        }

        return response, 200
