# -*- coding: utf-8 -*-

from flask_restful import reqparse

parser = reqparse.RequestParser()
parser.add_argument('dropboxOauthTuple', type=int, location='args')
