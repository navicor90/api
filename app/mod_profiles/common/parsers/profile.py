# -*- coding: utf-8 -*-

from flask_restful import reqparse

from app.mod_profiles.validators.generic_validators import is_boolean, is_valid_id, is_valid_previous_date, \
    string_without_int


# Parser general
parser = reqparse.RequestParser()
parser.add_argument('last_name', type=string_without_int, required=True)
parser.add_argument('first_name', type=string_without_int, required=True)
parser.add_argument('gender_id', type=is_valid_id)
parser.add_argument('birthday', type=is_valid_previous_date)
parser.add_argument('is_health_professional', type=is_boolean)

# Parser para recurso POST
parser_post = parser.copy()

# Parser para recurso PUT
parser_put = parser.copy()
