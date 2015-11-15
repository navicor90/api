# -*- coding: utf-8 -*-

from flask_restful import reqparse

from app.mod_profiles.validators.generic_validators import is_valid_id


# Parser general
parser = reqparse.RequestParser()
parser.add_argument('analysis_id', type=is_valid_id, required=True)
parser.add_argument('group_id', type=is_valid_id, required=True)

# Parser para recurso POST
parser_post = parser.copy()
parser_post.remove_argument('analysis_id')
