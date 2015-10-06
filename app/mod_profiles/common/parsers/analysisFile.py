# -*- coding: utf-8 -*-

from werkzeug.datastructures import FileStorage
from flask_restful import reqparse

from app.mod_profiles.validators.globalValidator import is_valid_id


# Parser general
parser = reqparse.RequestParser()
parser.add_argument('path', type=str, required=True)
parser.add_argument('description', type=str)
parser.add_argument('image_file', type=FileStorage, location='files', required=True)
parser.add_argument('analysis_id', type=is_valid_id, required=True)
parser.add_argument('storage_location_id', type=is_valid_id, required=True)

# Parser para recurso POST
parser_post = parser.copy()
parser_post.remove_argument('path')
parser_post.remove_argument('storage_location_id')

# Parser para recurso PUT
parser_put = parser.copy()
