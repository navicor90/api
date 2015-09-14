# -*- coding: utf-8 -*-

from flask_restful import reqparse
from app.mod_profiles.validators.globalValidator import string_without_int

# Parser general
parser = reqparse.RequestParser()
parser.add_argument('name', type=string_without_int, required=True)
parser.add_argument('symbol', type=string_without_int, required=True)
parser.add_argument('suffix', type=bool)

# Parser para recurso POST
parser_post = parser.copy()

# Parser para recurso PUT
parser_put = parser.copy()
