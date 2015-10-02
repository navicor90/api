# -*- coding: utf-8 -*-

from flask_restful import Resource, marshal_with
from flask_restful_swagger import swagger

from app.mod_shared.models.db import db
from app.mod_profiles.models import AnalysisFile
from app.mod_profiles.common.fields.analysisFileFields import AnalysisFileFields
from app.mod_profiles.common.parsers.analysisFile import parser_put


class AnalysisFileView(Resource):
    @swagger.operation(
        notes=u'Retorna una instancia específica de archivo de análisis.'.encode('utf-8'),
        responseClass='AnalysisFileFields',
        nickname='analysisFileView_get',
        parameters=[
            {
              "name": "id",
              "description": u'Identificador único del archivo de análisis.'.encode('utf-8'),
              "required": True,
              "dataType": "int",
              "paramType": "path"
            }
          ],
        responseMessages=[
            {
              "code": 200,
              "message": "Objeto encontrado."
            },
            {
              "code": 404,
              "message": "Objeto inexistente."
            }
          ]
        )
    @marshal_with(AnalysisFileFields.resource_fields, envelope='resource')
    def get(self, id):
        analysis_file = AnalysisFile.query.get_or_404(id)
        return analysis_file

    @swagger.operation(
        notes=(u'Actualiza una instancia específica de archivo de análisis, y '
               'la retorna.').encode('utf-8'),
        responseClass='AnalysisFileFields',
        nickname='analysisFileView_put',
        parameters=[
            {
              "name": "id",
              "description": u'Identificador único del archivo de análisis.'.encode('utf-8'),
              "required": True,
              "dataType": "int",
              "paramType": "path"
            },
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
              "code": 200,
              "message": "Objeto actualizado exitosamente."
            },
            {
              "code": 404,
              "message": "Objeto inexistente."
            }
          ]
        )
    @marshal_with(AnalysisFileFields.resource_fields, envelope='resource')
    def put(self, id):
        analysis_file = AnalysisFile.query.get_or_404(id)
        args = parser_put.parse_args()

        # Actualiza los atributos del objeto, en base a los argumentos
        # recibidos.

        # Actualiza la ruta del archivo, en caso de que haya sido modificada.
        if (args['path'] is not None and
              analysis_file.path != args['path']):
            analysis_file.path = args['path']
        # Actualiza la descripción, en caso de que haya sido modificada.
        if (args['description'] is not None and
              analysis_file.description != args['description']):
            analysis_file.description = args['description']
        # Actualiza el análisis asociado, en caso de que haya sido modificado.
        if (args['analysis_id'] is not None and
              analysis_file.analysis_id != args['analysis_id']):
            analysis_file.analysis_id = args['analysis_id']
        # Actualiza la ubicación de almacenamiento asociada, en caso de que
        # haya sido modificada.
        if (args['storage_location_id'] is not None and
              analysis_file.storage_location_id != args['storage_location_id']):
            analysis_file.storage_location_id = args['storage_location_id']

        db.session.commit()
        return analysis_file, 200
