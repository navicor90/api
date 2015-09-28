# -*- coding: utf-8 -*-

from app.mod_profiles.validators.globalValidator import is_valid_id
from flask_restful import reqparse

parser = reqparse.RequestParser()
parser.add_argument('location', type=is_valid_id())
parser.add_argument('user', type=is_valid_id)
