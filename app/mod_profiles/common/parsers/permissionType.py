# -*- coding: utf-8 -*-

from flask_restful import reqparse

from app.mod_profiles.validators.generic_validators import string_without_int


# Parser general
parser = reqparse.RequestParser()
parser.add_argument('name', type=string_without_int, required=True)
parser.add_argument('description', type=str, required=True)
parser.add_argument('can_view_analysis_files', type=bool, required=True)
parser.add_argument('can_view_measurements', type=bool, required=True)
parser.add_argument('can_edit_analysis_files', type=bool, required=True)
parser.add_argument('can_edit_measurements', type=bool, required=True)

# Parser para recurso POST
parser_post = parser.copy()

# Parser para recurso PUT
parser_put = parser.copy()
