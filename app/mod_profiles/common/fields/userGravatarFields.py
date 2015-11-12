# -*- coding: utf-8 -*-

from flask_restful import fields
from flask_restful_swagger import swagger


@swagger.model
class UserGravatarFields:
    resource_fields = {
        'gravatar_url': fields.String,
    }
