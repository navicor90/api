# -*- coding: utf-8 -*-

from flask_restful import reqparse

from app.mod_profiles.validators.generic_validators import is_valid_id, string_without_int


# Parser general
parser = reqparse.RequestParser()
parser.add_argument('name', type=string_without_int, required=True)
parser.add_argument('description', type=str)

# Parser para recurso POST
parser_post = parser.copy()
parser_post.add_argument('group_membership_type_id', type=is_valid_id, required=True)
parser_post.add_argument('permission_type_id', type=is_valid_id, required=True)

# Parser para recurso PUT
parser_put = parser.copy()
