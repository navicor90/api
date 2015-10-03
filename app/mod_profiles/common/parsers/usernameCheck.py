# -*- coding: utf-8 -*-

from flask_restful import reqparse


# Parser general
parser = reqparse.RequestParser()
parser.add_argument('username', type=str, required=True)

# Parser para recurso GET
parser_get = parser.copy()
