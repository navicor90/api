# -*- coding: utf-8 -*-

from datetime import datetime
from app.mod_profiles.common.fields.analysisFileFields import AnalysisFileFields
from app.mod_profiles.models.AnalysisFile import AnalysisFile
from app.mod_shared.models.db import db
from flask.ext.restful import marshal_with
from flask_restful import Resource
from app.mod_profiles.common.parsers.analysysFileUpload import parser_post
from app.mod_profiles.adapters.fileManagerFactory import FileManagerFactory
from flask.helpers import flash
from app.mod_profiles.models import User
from app.mod_profiles.common.persistence import storageLocation


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
        file_manager = FileManagerFactory().get_file_manager(user)
        res = file_manager.upload_file(image_file)
        storage_location = storageLocation.get_by_name(res['storage_location'])
        new_analysis_file = AnalysisFile(datetime.utcnow(),
                                         res['path'],
                                         res['description'],
                                         args['analysis_id'],
                                         storage_location.id)
        db.session.add(new_analysis_file)
        db.session.commit()
        return new_analysis_file, 201