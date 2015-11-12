# -*- coding: utf-8 -*-

from flask_restful import reqparse

from app.mod_profiles.validators.generic_validators import positive_int


# Parser general
parser = reqparse.RequestParser()
parser.add_argument('default', type=str)
parser.add_argument('size', type=positive_int)

# Parser para recurso GET
parser_get = parser.copy()
