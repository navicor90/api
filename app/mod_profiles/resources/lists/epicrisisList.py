# -*- coding: utf-8 -*-

from flask_restful import Resource, marshal_with
from app.mod_profiles.common.fields.epicrisisFields import EpicrisisFields
from app.mod_profiles.common.parsers.epicrisis import parser_post
from app.mod_profiles.adapters.fileManagerFactory import FileManagerFactory
from flask.helpers import flash

class EpicrisisList(Resource):

    @marshal_with(EpicrisisFields.resource_fields, envelope='resource')
    def post(self):
        args = parser_post.parse_args()
        image_file = args['image']
        if image_file is None:
            # Tendría que ser reemplazado por un response adecuado
            flash("Debe cargar un archivo")
        file_manager = FileManagerFactory().get_file_manager('Dropbox')
        file_manager.upload_file(image_file, args['datetime'])



