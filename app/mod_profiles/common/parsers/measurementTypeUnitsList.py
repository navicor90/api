# -*- coding: utf-8 -*-

from flask_restful import reqparse

from app.mod_profiles.validators.globalValidator import is_valid_id


# Parser general
parser = reqparse.RequestParser()
parser.add_argument('measurement_unit_id_list', type=is_valid_id, required=True, action='append')

# Parser para recurso PUT
parser_put = parser.copy()
