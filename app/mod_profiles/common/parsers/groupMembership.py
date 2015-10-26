# -*- coding: utf-8 -*-

from flask_restful import reqparse

from app.mod_profiles.validators.generic_validators import is_valid_id, is_boolean


# Parser general
parser = reqparse.RequestParser()
parser.add_argument('is_admin', type=is_boolean, required=True)
parser.add_argument('group_id', type=is_valid_id, required=True)
parser.add_argument('group_membership_type_id', type=is_valid_id, required=True)
parser.add_argument('permission_type_id', type=is_valid_id, required=True)
parser.add_argument('profile_id', type=is_valid_id, required=True)

# Parser para recurso POST
parser_post = parser.copy()

# Parser para recurso PUT
parser_put = parser.copy()
parser_put.remove_argument('group_id')
parser_put.remove_argument('profile_id')

# Parser para recurso POST con usuario autenticado
parser_post_auth = parser.copy()
parser_post_auth.remove_argument('group_id')
parser_post_auth.remove_argument('profile_id')
parser_post_auth.add_argument('user_id', type=is_valid_id, required=True)
