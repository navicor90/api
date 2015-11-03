# -*- coding: utf-8 -*-

from flask_restful import reqparse

from app.mod_profiles.validators.generic_validators import is_valid_id


# Parser general
parser = reqparse.RequestParser()
parser.add_argument('profile', type=is_valid_id)

# Parser para recurso GET
parser_get = parser.copy()
