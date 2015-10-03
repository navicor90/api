# -*- coding: utf-8 -*-

from datetime import datetime
from flask_restful import Resource, marshal_with
from flask_restful_swagger import swagger

from app.mod_shared.models.db import db
from app.mod_profiles.models import AnalysisFile
from app.mod_profiles.common.fields.analysisFileFields import AnalysisFileFields
from app.mod_profiles.common.parsers.analysisFile import parser_post


class AnalysisFileList(Resource):
    @swagger.operation(
        notes=(u'Retorna todas las instancias existentes de archivos de '
               'análisis.').encode('utf-8'),
        responseClass='AnalysisFileFields',
        nickname='analysisFileList_get',
        responseMessages=[
            {
              "code": 200,
              "message": "Solicitud resuelta exitosamente."
            }
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
              "name": "path",
              "description": u'Ruta al archivo de análisis.'.encode('utf-8'),
              "required": True,
              "dataType": "string",
              "paramType": "body"
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
            },
            {
              "name": "storage_location_id",
              "description": (u'Identificador único de la ubicación de '
                              'almacenamiento asociada.').encode('utf-8'),
              "required": True,
              "dataType": "int",
              "paramType": "body"
            }
          ],
        responseMessages=[
            {
              "code": 201,
              "message": "Objeto creado exitosamente."
            }
          ]
        )
    @marshal_with(AnalysisFileFields.resource_fields, envelope='resource')
    def post(self):
        args = parser_post.parse_args()
        new_analysis_file = AnalysisFile(datetime.utcnow(),
                                         args['path'],
                                         args['description'],
                                         args['analysis_id'],
                                         args['storage_location_id'])
        db.session.add(new_analysis_file)
        db.session.commit()
        return new_analysis_file, 201
