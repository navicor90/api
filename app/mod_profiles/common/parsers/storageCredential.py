# -*- coding: utf-8 -*-

from flask_restful import reqparse
from app.mod_profiles.validators.globalValidator import is_valid_id

# Parser general
parser = reqparse.RequestParser()
parser.add_argument('token', type=str, required=True)
parser.add_argument('owner_id', type=is_valid_id, required=True)
parser.add_argument('storage_location_id', type=is_valid_id, required=True)

# Parser para recurso POST
parser_post = parser.copy()

# Parser para recurso PUT
parser_put = parser.copy()