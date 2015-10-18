# -*- coding: utf-8 -*-

from flask_restful import reqparse
from app.mod_profiles.validators.generic_validators import is_valid_id

# Parser general
parser = reqparse.RequestParser()
parser.add_argument('comment', type=str, required=True)
parser.add_argument('analysis_id', type=is_valid_id, required=True)
parser.add_argument('profile_id', type=is_valid_id, required=True)

# Parser para recurso POST
parser_post = parser.copy()

# Parser para recurso PUT
parser_put = parser.copy()

# Parser para recurso POST con usuario autenticado
parser_post_auth = parser.copy()
parser_post_auth.remove_argument('analysis_id')
parser_post_auth.remove_argument('profile_id')

# Parser para recurso PUT con usuario autenticado
parser_put_auth = parser.copy()
parser_put_auth.remove_argument('analysis_id')
parser_put_auth.remove_argument('profile_id')
