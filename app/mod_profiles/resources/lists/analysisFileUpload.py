# -*- coding: utf-8 -*-

from datetime import datetime
from flask.helpers import flash
from flask_restful import Resource, marshal_with

from app.mod_shared.models.db import db
from app.mod_profiles.adapters import FileManagerFactory
from app.mod_profiles.common.fields.analysisFileFields import AnalysisFileFields
from app.mod_profiles.common.parsers.analysisFileUpload import parser_post
from app.mod_profiles.models import AnalysisFile, StorageLocation, User


class AnalysisFileUpload(Resource):

    @marshal_with(AnalysisFileFields.resource_fields, envelope='resource')
    def post(self):
        args = parser_post.parse_args()
        # En lugar de recibir el id del user tendría que tomar el user a partir del objeto de
        # contexto g de flask
        user = User.query.get_or_404(args['user_id'])
        image_file = args['image_file']
        if image_file is None:
            # Tendría que ser reemplazado por un response adecuado
            flash("Debe cargar un archivo")
            return '', 400

        file_manager = FileManagerFactory().get_file_manager(user)
        res = file_manager.upload_file(image_file)
        storage_location = StorageLocation.query.filter_by(name=res['storage_location']).first()
        if storage_location is None:
            raise ValueError("No se encuentra una ubicación con la denominación especificada.")

        new_analysis_file = AnalysisFile(datetime.utcnow(),
                                         res['path'],
                                         res['description'],
                                         args['analysis_id'],
                                         storage_location.id)
        db.session.add(new_analysis_file)
        db.session.commit()
        return new_analysis_file, 201