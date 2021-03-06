# -*- coding: utf-8 -*-

from flask_restful import reqparse

from app.mod_profiles.validators.generic_validators import is_valid_id, is_valid_previous_datetime


# Parser general
parser = reqparse.RequestParser()
parser.add_argument('min_value', type=float, required=True)
parser.add_argument('max_value', type=float, required=True)
parser.add_argument('measurement_type_id', type=is_valid_id, required=True)
parser.add_argument('measurement_unit_id', type=is_valid_id, required=True)

# Parser para recurso POST
parser_post = parser.copy()
parser_post.remove_argument('measurement_type_id')

# Parser para recurso PUT
parser_put = parser.copy()
