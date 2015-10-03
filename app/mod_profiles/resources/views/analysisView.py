# -*- coding: utf-8 -*-

from flask_restful import Resource, marshal_with
from flask_restful_swagger import swagger

from app.mod_shared.models.db import db
from app.mod_profiles.models import Analysis
from app.mod_profiles.common.fields.analysisFields import AnalysisFields
from app.mod_profiles.common.parsers.analysis import parser_put
from app.mod_profiles.common.swagger.responses.generic_responses import code_200_found, code_200_updated, code_404


class AnalysisView(Resource):
    @swagger.operation(
        notes=u'Retorna una instancia específica de análisis.'.encode('utf-8'),
        responseClass='AnalysisFields',
        nickname='analysisView_get',
        parameters=[
            {
              "name": "id",
              "description": u'Identificador único del análisis.'.encode('utf-8'),
              "required": True,
              "dataType": "int",
              "paramType": "path"
            }
          ],
        responseMessages=[
            code_200_found,
            code_404
        ]
    )
    @marshal_with(AnalysisFields.resource_fields, envelope='resource')
    def get(self, id):
        analysis = Analysis.query.get_or_404(id)
        return analysis

    @swagger.operation(
        notes=u'Actualiza una instancia específica de análisis, y la retorna.'.encode('utf-8'),
        responseClass='AnalysisFields',
        nickname='analysisView_put',
        parameters=[
            {
              "name": "id",
              "description": u'Identificador único del análisis.'.encode('utf-8'),
              "required": True,
              "dataType": "int",
              "paramType": "path"
            },
            {
              "name": "datetime",
              "description": u'Fecha y hora del análisis.'.encode('utf-8'),
              "required": True,
              "dataType": "datetime",
              "paramType": "body"
            },
            {
              "name": "description",
              "description": u'Descripción del análisis.'.encode('utf-8'),
              "required": True,
              "dataType": "string",
              "paramType": "body"
            },
            {
              "name": "profile_id",
              "description": u'Identificador único del perfil asociado.'.encode('utf-8'),
              "required": True,
              "dataType": "int",
              "paramType": "body"
            }
          ],
        responseMessages=[
            code_200_updated,
            code_404
        ]
    )
    @marshal_with(AnalysisFields.resource_fields, envelope='resource')
    def put(self, id):
        analysis = Analysis.query.get_or_404(id)
        args = parser_put.parse_args()

        # Actualiza los atributos del objeto, en base a los argumentos
        # recibidos.

        # Actualiza la fecha y hora del análisis, en caso de que haya sido
        # modificado.
        if (args['datetime'] is not None and
              analysis.datetime != args['datetime']):
            analysis.datetime = args['datetime']
        # Actualiza la descripción, en caso de que haya sido modificada.
        if (args['description'] is not None and
              analysis.description != args['description']):
            analysis.description = args['description']
        # Actualiza el perfil asociado, en caso de que haya sido modificado.
        if (args['profile_id'] is not None and
              analysis.profile_id != args['profile_id']):
            analysis.profile_id = args['profile_id']

        db.session.commit()
        return analysis, 200
