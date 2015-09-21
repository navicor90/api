# -*- coding: utf-8 -*-

from flask_restful import reqparse
from app.mod_profiles.validators.globalValidator import is_valid_datetime
import werkzeug

parser = reqparse.RequestParser()
parser.add_argument('datetime', type=is_valid_datetime, required=True)
parser.add_argument('image', type=werkzeug.datastructures.FileStorage, location='files')
parser_post = parser
