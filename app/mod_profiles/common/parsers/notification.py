# -*- coding: utf-8 -*-

from flask_restful import reqparse

from app.mod_profiles.validators.generic_validators import is_boolean, positive_int


# Parser general
parser = reqparse.RequestParser()
parser.add_argument('quantity', type=positive_int)
parser.add_argument('unread', type=is_boolean)

# Parser para recurso GET
parser_get = parser.copy()
