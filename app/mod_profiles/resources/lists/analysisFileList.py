# -*- coding: utf-8 -*-

from datetime import datetime
from flask import g
from flask_restful import Resource, marshal_with
from flask_restful_swagger import swagger

from app.mod_shared.models.auth import auth
from app.mod_shared.models.db import db
from app.mod_profiles.adapters.fileManagerFactory import FileManagerFactory
from app.mod_profiles.models import Analysis, AnalysisFile, StorageLocation
from app.mod_profiles.common.fields.analysisFileFields import AnalysisFileFields
from app.mod_profiles.common.parsers.analysisFile import parser_post
from app.mod_profiles.common.persistence import permission
from app.mod_profiles.common.swagger.responses.generic_responses import code_200_ok, code_201_created, code_401, \
    code_403


class AnalysisFileList(Resource):
    @swagger.operation(
        notes=(u'Retorna todas las instancias existentes de archivos de '
               'análisis.').encode('utf-8'),
        responseClass='AnalysisFileFields',
        nickname='analysisFileList_get',
        responseMessages=[
            code_200_ok
        ]
    )
    @marshal_with(AnalysisFileFields.resource_fields, envelope='resource')
    def get(self):
        analysis_files = AnalysisFile.query.all()
        return analysis_files

    @swagger.operation(
        notes=u'Crea una nueva instancia de archivo de análisis, y la retorna.'.encode('utf-8'),
        responseClass='AnalysisFileFields',
        nickname='analysisFileList_post',
        parameters=[
            {
                "name": "image_file",
                "description": u'Archivo de análisis.'.encode('utf-8'),
                "required": True,
                "dataType": "file",
                "paramType": "form"
            },
            {
                "name": "description",
                "description": u'Descripción del archivo de análisis.'.encode('utf-8'),
                "required": False,
                "dataType": "string",
                "paramType": "body"
            },
            {
                "name": "analysis_id",
                "description": u'Identificador único del análisis asociado.'.encode('utf-8'),
                "required": True,
                "dataType": "int",
                "paramType": "body"
            }
        ],
        responseMessages=[
            code_201_created,
            code_401,
            code_403
        ]
    )
    @auth.login_required
    @marshal_with(AnalysisFileFields.resource_fields, envelope='resource')
    def post(self):
        # Obtiene los valores de los argumentos recibidos en la petición.
        args = parser_post.parse_args()
        image_file = args['image_file']
        description = args['description']
        analysis_id = args['analysis_id']

        # Obtiene el análisis especificado.
        analysis = Analysis.query.get_or_404(analysis_id)

        # Verifica que el usuario autenticado tenga permiso para editar los
        # archivos de análisis, del análisis especificado.
        if not permission.get_permission_by_user(analysis, g.user, 'edit_analysis_files'):
            return '', 403

        file_manager = FileManagerFactory().get_file_manager(g.user)
        res = file_manager.upload_file(image_file)
        storage_location = StorageLocation.query.filter_by(name=res['storage_location']).first()
        if storage_location is None:
            raise ValueError("No se encuentra una ubicación con la denominación especificada.")

        new_analysis_file = AnalysisFile(datetime.utcnow(),
                                         res['path'],
                                         description,
                                         analysis.id,
                                         storage_location.id)
        db.session.add(new_analysis_file)
        db.session.commit()
        return new_analysis_file, 201
