# -*- coding: utf-8 -*-

from flask_restful import reqparse

from app.mod_profiles.validators.globalValidator import is_valid_id


# Parser general
parser = reqparse.RequestParser()
parser.add_argument('source', type=is_valid_id)
parser.add_argument('type', type=is_valid_id)
parser.add_argument('unit', type=is_valid_id)

# Parser para recurso GET
parser_get = parser.copy()
