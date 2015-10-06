# -*- coding: utf-8 -*-

import werkzeug
from werkzeug.datastructures import FileStorage
from flask_restful import reqparse

from app.mod_profiles.validators.globalValidator import is_valid_id


# Parser general
parser = reqparse.RequestParser()
parser.add_argument('user_id', type=is_valid_id)
parser.add_argument('analysis_id', type=is_valid_id)
parser.add_argument('image_file', type=werkzeug.datastructures.FileStorage, location='files')

# Parser para recurso POST
parser_post = parser.copy()
